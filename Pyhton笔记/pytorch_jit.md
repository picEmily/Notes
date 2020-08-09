# JIT
## JIT原理
[Pytorch IR](https://github.com/pytorch/pytorch/wiki/PyTorch-IR)
- graph
- block
- node
- value

## pytorch JIT 源码
参考：https://zasdfgbnm.github.io/2018/09/20/PyTorch-JIT-Source-Code-Read-Note/

我看的是torch==1.2
- ctx:context
- ast:abstract syntax tree https://en.wikipedia.org/wiki/Abstract_syntax_tree

主要函数：
- ``__init__.py``:``script()``,``script_method()``
- ``fronted.py``:

### init.py
scripting a function/class
```
def script(obj, optimize=None, _frames_up=0, _rcb=None):
    if not _enabled:
        return obj

    if optimize is not None:
        warnings.warn("`optimize` is deprecated and has no effect. Use `with torch.jit.optimized_execution() instead")

    torch._C._clear_compilation_stack_DELETEME()
    if isinstance(obj, torch.nn.Module):
        return _convert_to_script_module(obj)

    qualified_name = _qualified_name(obj)
    if inspect.isclass(obj):
        # If this type is a `nn.Module` subclass, they probably meant to pass
        # an instance instead of a Module
        if issubclass(obj, torch.nn.Module):
            raise RuntimeError("Type '{}' cannot be compiled since it inherits"
                               " from nn.Module,"
                               " pass an instance instead".format(obj))

        if not _is_new_style_class(obj):
            raise RuntimeError("TorchScript classes must be new-style classes. "
                               "Please inherit from 'object'")
        if _rcb is None:
            _rcb = _jit_internal.createResolutionCallback(_frames_up + 1)
        _compile_and_register_class(obj, _rcb, qualified_name)
        return obj
    else:
        return _compile_function(fn=obj, qualified_name=qualified_name, _frames_up=_frames_up + 1, _rcb=_rcb)

def _compile_function(fn, qualified_name, _frames_up, _rcb=None):
    ast = get_jit_def(fn)
    if _rcb is None:
        closure_rcb = _jit_internal.createResolutionCallbackFromClosure(fn)
        stack_rcb = _jit_internal.createResolutionCallback(_frames_up + 1)

        def _rcb(name):
            # since type comments aren't captured in the function's closures,
            # we still need to try to the rcb based on stack frames if the
            # closure rcb fails
            result = closure_rcb(name)
            if result:
                return result
            return stack_rcb(name)
    script_fn = torch._C._jit_script_compile(qualified_name, ast, _rcb, get_default_args(fn))
    # Forward docstrings
    script_fn.__doc__ = fn.__doc__
    return script_fn
```
新版本可以script function/class比较复杂一点，先看老版本只可以用script function
```python3
def script(fn, optimize=True, _frames_up=0):
    if not _enabled:
        return fn
    rcb = createResolutionCallback(_frames_up + 1)  # 返回一个接受字符串（函数名）参数的函数
    ast = get_jit_ast(fn, is_method=False)  # 抽象语法树
    graph = _jit_script_compile(ast, rcb)  # 会调用C++的方法，用C++编译，新版把graph拆走了
    mod = ScriptModule()
    mod._create_method_from_graph('forward', graph)  # 一个普通函数变成了ScriptModule()的方法
    # TODO: refactor everything so we're not 1) creating a ScriptModule
    # 2) Throwing everything away except for the graph 3) Creating a new
    # ScriptModule and dumping that graph in 4) Re-populating the schema
    # because it was lost doing the previous
    mod.__getattr__('forward').forward_schema(ast, False)
    # Forward docstrings
    mod.__doc__ = fn.__doc__
    return mod
```
``createResolutionCallback()``: 官方文档

> Creates a function which, given a string variable name,
> returns the value of the variable in the scope of the caller of
> the function which called createResolutionCallback (by default).
> 
> This is used to enable access in-scope Python variables inside
> TorchScript fragments.
> 
> frames_up is number of additional frames to go up on the stack.
> The default value is 0, which correspond to the frame of the caller
> of createResolutionCallback. Also for example, if frames_up is set
> to 1, then the frame of the caller's caller of createResolutionCallback
> will be taken.

For example, the following program prints 2:

    def bar():
        cb = createResolutionCallback(1)
        print(cb("foo"))

    def baz():
        foo = 2
        bar()

    baz()


TODO: 新版本script()类分析

```python3
def script_method(fn, _rcb=None):
    if not _enabled:
        return fn
    # NOTE: we need to traverse two frames here because the meta-class frame
    # for ScriptModule will be present, as opposed to invoking @script on a
    # a function or invoking define() on a CompilationUnit.
    # The stack will look like:
    #
    # 0. createResolutionCallback()
    # 1. script_method()
    # 2. ScriptModule metaclass frame
    # 3. Surrounding scope
    #
    # createResolutionCallback internally adds 1 to get us to the scope of this
    # function (the calling function). Adding 2 gets us to the proper surrounding scope.
    if _rcb is None:
        _rcb = _jit_internal.createResolutionCallback(frames_up=2)  # 相当于读了类属性
    ast = get_jit_def(fn, self_name="ScriptModule")
    return ScriptMethodStub(_rcb, ast, fn)

ScriptMethodStub = namedtuple('ScriptMethodStub', ('resolution_callback', 'def_', 'original_method'))

# namedtuple(typename, field_names, *, verbose=False, rename=False, module=None)
# Returns a new subclass of tuple with named fields. 
# 大概就是把tuple变成一个类，两个参数是tuple的两个elements
```
it is not callable, 所以接下来是ScriptMeta()类做的（学习class meta-programming）。将其变成callable 的方法是

搬运https://zasdfgbnm.github.io/2018/09/20/PyTorch-JIT-Source-Code-Read-Note/
```
class MyModule(torch.jit.ScriptModule):
    @torch.jit.script_method
    def f(self.x):
        return x * x
    @torch.jit.script_method
    def forward(self, x):
        return x + self.f(x)
```
> It will execute the body of the class definition, that is: compile the ``return x * x``, create an function object with that compiled code, pass this function object to ``torch.jit.script_method``, and set the returned named tuple as f. Then do the same thing for forward. After that, Python will have a map of attribute names and values of the class to be constructed. This map will then be passed to the meta-class of MyModule to actually construct MyModule as an instance of that meta-class.

### ``frontend.py``
这里主要是怎么处理我的python代码，把其处理以后再交给下一层(一般在``__init__.py``里面)处理成torchscript,编译等等。

``is_reserved_name()``:接受哪些关键字，用来构建ast

```python3
def get_jit_def(fn, self_name=None):
    sourcelines, file_lineno = inspect.getsourcelines(fn)  # 得到fn里面的live objs 
    source = ''.join(sourcelines)
    filename = inspect.getsourcefile(fn)
    dedent_src = dedent(source)
    py_ast = ast.parse(dedent_src)
    if len(py_ast.body) != 1 or not isinstance(py_ast.body[0], ast.FunctionDef):
        raise RuntimeError("expected a single top-level function")
    leading_whitespace_len = len(source.split('\n', 1)[0]) - len(dedent_src.split('\n', 1)[0])
    type_line = torch.jit.annotations.get_type_line(source)  # 读type，不写的话默认torch.Tensor
    ctx = SourceContext(source, filename, file_lineno, leading_whitespace_len, _uses_true_division(fn))
    return build_def(ctx, py_ast.body[0], type_line, self_name)
```
> ``inspect`` module: get information about live objects such as modules, classes, methods, functions, tracebacks, frame objects, and code objects. 
> ``textwrap.dedent(text)``: 不要indent
> ``ast`` module: process trees of the Python abstract syntax grammar. An abstract syntax tree can be compiled into a Python code object using the built-in compile() function.

```python3
def build_def(ctx, py_def, type_line, self_name=None):
    body = py_def.body
    r = ctx.make_range(py_def.lineno, py_def.col_offset,
                       py_def.col_offset + len("def"))
    param_list = build_param_list(ctx, py_def.args, self_name)
    return_type = None
    if getattr(py_def, 'returns', None) is not None:
        return_type = build_expr(ctx, py_def.returns)
    decl = Decl(r, param_list, return_type)
    is_method = self_name is not None
    if type_line is not None:
        type_comment_decl = torch._C.parse_type_comment(type_line)
        decl = torch._C.merge_type_from_type_comment(decl, type_comment_decl, is_method)
    return Def(Ident(r, py_def.name),
               decl,
               build_stmts(ctx, body))
```
> Reading through this, we can see that what basically this does is to convert the Python’s AST into the internal representation. Names like Decl, Def, Ident are all imported by from ``torch._C._jit_tree_views import *``. 


``StmtBuilder()``:一个用来build各种statement
``ExprBuilder()``:差不多


# TorchScript使用
参考：
https://pytorch.org/docs/stable/jit.html
https://pytorch.org/tutorials/advanced/cpp_export.html
https://github.com/huggingface/pytorch-transformers/blob/master/docs/source/torchscript.rst
https://pytorch.org/tutorials/beginner/deploy_seq2seq_hybrid_frontend_tutorial.html

TorchScript is a way to create serializable and optimizable models from PyTorch code. Any code written in TorchScript can be saved from a Python process and loaded in a process where there is no Python dependency.

We provide tools to incrementally **transition a model from a pure Python program to a TorchScript program that can be run independently from Python, for instance, in a standalone C++ program.** This makes it possible to train models in PyTorch using familiar tools and then export the model via TorchScript to a production environment where it is not a good idea to run models as Python programs for performance and multi-threading reasons.

把纯python代码经过简单的修饰，变成TorchScript对象，导出并用c++编译（也可以不用），达到加速的目的。

## ``Class torch.jit.ScriptModule (optimize=True)``
- 这个类，是我们改造pytorch代码的关键（成为**TorchScript functions**）
- model->a tree of submodules
- 每个部分都可以有子模块，参数，方法
- 主要方法:``tracing`` , ``scripting``

### tracing
包装一个方法，可以直接把其变成ScriptModule，并有一个forward方法。

> NOTE
> 
> Tracing only records operations done when the given function is run on the given tensors. Therefore, the returned ScriptModule will always run the same traced graph on any input. This has some important implications when your module is expected to run different sets of operations, depending on the input and/or the module state. For example,
> 
> Tracing will not record any control-flow like if-statements or loops. When this control-flow is constant across your module, this is fine and it often inlines the control-flow decisions. But sometimes the control-flow is actually part of the model itself. For instance, a recurrent network is a loop over the (possibly dynamic) length of an input sequence.
> 
> In the returned ScriptModule, operations that have different behaviors in training and eval modes will always behave as if it is in the mode it was in during tracing, no matter which mode the ScriptModule is in.
> 
> In cases like these, tracing would not be appropriate and scripting is a better choice.

如果方法中有流程，要用script，即将python编译成TorchScript对象。

### Scripting:
装饰器，装饰函数/方法，也是变成ScriptModule 类，然后成为TorchScript代码

个人理解：trace用来包一个nn.module里面的方法
scripting用来写自己模型里的forward

或：``sm = torch.jit.script(my_module)``

限制：
- All functions must be valid TorchScript functions (including __init__())
- Classes must be new-style classes, as we use __new__() to construct them with pybind11
- TorchScript classes are statically typed. Members are declared by assigning to self in the __init__() method
- No expressions except method definitions are allowed in the body of the class
- No support for inheritance or any other polymorphism strategy, except for inheriting from object to specify a new-style class

## Combination of trace and script
可以互相包
- script 包 trace:(？？？使用场景？？？)
- trace 包 script: 有控制流程，写在script里面，再用trace包

> 动态图，静态图区别
> https://wizardforcel.gitbooks.io/learn-dl-with-pytorch-liaoxingyu/2.3.html
> 我理解trace有点静态图的感觉，不可以用在可控制流程里面

## save and load
save之后可以被c++或者其他python运行

## c编译
C++和python运行jit的速度差不多

### cmake
https://blog.csdn.net/libaineu2004/article/details/77119908

## debug
TorchScript is a statically typed subset of Python
所以依旧可以用debug python的方法来debug

环境变量： 
``PYTORCH_JIT=1``
``PYTORCH_JIT=0`` will disable all script and tracing annotations. If there is hard-to-debug error in one of your ScriptModules, you can use this flag to force everything to run using native Python. This allows the use of tools like pdb to debug code.

对于forward的方法
``print(foo.code)``来看方法是不是和自己想的一样

局限：
TorchScript focuses specifically on the features of Python that are needed to represent neural network models in Torch.
所以有些限制
- 不支持所有python功能
	- 数据类型只有少数几种
- 不需要声明变量但是变量类型一旦分配了就不能变。默认类型是Tensor，建议使用``type``
- List,Dict 用``torch.jit.annotate``包装

# NLP学习笔记
## BertModel
输入参数: 参考huggingface的源码``modeling_bert.py``
```
BERT_INPUTS_DOCSTRING = r"""
    Inputs:
        **input_ids**: ``torch.LongTensor`` of shape ``(batch_size, sequence_length)``:
            Indices of input sequence tokens in the vocabulary.
            To match pre-training, BERT input sequence should be formatted with [CLS] and [SEP] tokens as follows:

            (a) For sequence pairs:

                ``tokens:         [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]``
                
                ``token_type_ids:   0   0  0    0    0     0       0   0   1  1  1  1   1   1``

            (b) For single sequences:

                ``tokens:         [CLS] the dog is hairy . [SEP]``
                
                ``token_type_ids:   0   0   0   0  0     0   0``
    
            Indices can be obtained using :class:`pytorch_transformers.BertTokenizer`.
            See :func:`pytorch_transformers.PreTrainedTokenizer.encode` and
            :func:`pytorch_transformers.PreTrainedTokenizer.convert_tokens_to_ids` for details.
        **position_ids**: (`optional`) ``torch.LongTensor`` of shape ``(batch_size, sequence_length)``:
            Indices of positions of each input sequence tokens in the position embeddings.
            Selected in the range ``[0, config.max_position_embeddings - 1[``.
        **token_type_ids**: (`optional`) ``torch.LongTensor`` of shape ``(batch_size, sequence_length)``:
            Segment token indices to indicate first and second portions of the inputs.
            Indices are selected in ``[0, 1]``: ``0`` corresponds to a `sentence A` token, ``1``
            corresponds to a `sentence B` token
            (see `BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding`_ for more details).
        **attention_mask**: (`optional`) ``torch.Tensor`` of shape ``(batch_size, sequence_length)``:
            Mask to avoid performing attention on padding token indices.
            Mask values selected in ``[0, 1]``:
            ``1`` for tokens that are NOT MASKED, ``0`` for MASKED tokens.
        **head_mask**: (`optional`) ``torch.Tensor`` of shape ``(num_heads,)`` or ``(num_layers, num_heads)``:
            Mask to nullify selected heads of the self-attention modules.
            Mask values selected in ``[0, 1]``:
            ``1`` indicates the head is **not masked**, ``0`` indicates the head is **masked**.
```


## seq2seq
https://pytorch.org/tutorials/beginner/deploy_seq2seq_hybrid_frontend_tutorial.html
encoding and decoding

- encoding部分：
	- The encoder RNN **iterates through the input sentence one token (e.g. word)** at a time, at each time step outputting an “**output**” vector and a “**hidden** state” vector. The hidden state vector is then passed to the next time step, while the output vector is recorded. The encoder transforms the context it saw at each point in the sequence into a set of points in a high-dimensional space, which the decoder will use to generate a meaningful output for the given task.
	- embedding:把词搞成高维向量，output size = [batch_size, dimensions]
	- 几个重要参数：
		- text：我的句子
		- tokenized_text:分词之后的text -> List
		- indexed_tokens:每个词都有自己的idx，tokenized_text转换成用idx存储
		- attn_mask/mask: 某种注意力策略，1代表这个位置被注意了
		- outputs：batch_size 个向量，将用它们decode成为新的句子
- decoding部分：
	- The decoder RNN generates the response sentence in a token-by-token fashion. It uses the encoder’s context vectors, and internal hidden states to generate the next word in the sequence. It continues generating words until it outputs an EOS_token, representing the end of the sentence.  
	- 根据outputs逐个生成新词（简单一点的比如使用贪心策略）
- trace的注意：Notice that we initialize and load parameters into our encoder and decoder models as usual. If you are using tracing mode(torch.jit.trace) for some part of your models, you must call .to(device) to set the device options of the models and .eval() to set the dropout layers to test mode before tracing the models. TracedModule objects do not inherit the to or eval methods. Since in this tutorial we are only using scripting instead of tracing, we only need to do this before we do evaluation (which is the same as we normally do in eager mode).

# 笔记(1.1.0)
**原理：**

> For each user-defined class that subclasses ScriptModule this meta-class,
> (1) finds all the methods annotated with @script_method
> in a ScriptModule and removes them from the class attributes, and
> (2) puts a wrapper around the class's __init__ method to register
> all of the script_methods with the module after the original __init__
> has run. This has to occur after the user-defined __init__ so that
> submodules and parameters are initialized _before_ the script compiler
> resolve references to `self.param` or `self.module`.

**踩坑：**
- trace要传入example input，example input只有第0维可以变，其他的要和正式使用时相同。
- 能打出graph来至少说明转化成C++编译没问题
- for each loop 只能For loops over tuples; for xxx in range(10):
- for each loop in: dict支持keys
- 用script设计编译，分配内存的问题，所以要指定type
- 流程控制
	- 不能有continue, break（torch==1.2.0可以）
	- 只能是bool, int, float, or Tensor控制流程
	- xxx in xxx 不可以，只有dict可以
- How do I store attributes on a ScriptModule?
	- 见文档最后一条qa
	- attributes能传进去
	- Module Attributes 保存在外面
	- __constants__ (不能是dict) 
- ValueError: substring not found
	- 不要写中文注释
	- 可能原因出在for loop, 把graph打出来看一看，肯能是因为创建一个list是静态的，不能append两次（只有tensor才可以）
	- 这个里面定义的list不是list，而更像array，如果元素不是tensor要定义长度
- basic_string::at: __n (which is 18446744073709551615) >= this->size() (which is 6):
	- 某些index取到了-1
- UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe4 in position 0: unexpected end of data
	- jit全程使用utf-8，所以遇到中文很蛋疼（中文占3个字节，英文只占1个）


