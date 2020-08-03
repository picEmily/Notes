# 配置
- 设置中找到Interpreter->SSH Interpreter设置host和user。SSH成功以后能在server上找python解释器(一般会用conda或virtualenv建一个虚拟环境)
- 创建项目使用刚刚找到的解释器
- Tools->Deployment 可以上传或设置自动同步(ctrl+shift+x可以上传，在文件夹上使用能上传整个文件夹) 
- 设置本地和服务器代码同步，需要设置文件映射：Tools->Deployment->Configuration->mapping
- 将运行和debug环境换成服务器环境，也需要设置文件的映射：Run->Edit Configurations
- 设置环境变量：忘了，大概server上的这里读不到，pycharm有地方可以设置run时候的环境变量

# 技巧
- 即使自动同步了也每次手动上传一下
- git在本地操作会方便一点，server上不留下git，通过pycharm同步代码
- 这里使用的是本地编辑代码->pycharm上传代码到server->通过server上的解释器运行的方法。也可以直接打开server上的代码编辑(vscode的做法)，但是不推荐。