# 父子组件的沟通

## 父组件通过 Prop 向子组件传递数据

```vue
// 父组件 Father.vue

// 子组件 Son.vue
```



## 监听子组件事件

- 子组件调用 ``$emit()`` 将发送事件给父组件监听
- 好像是没有方法直接传值，子穿父只能通过监听事件的方式

```vue
// 父组件 Father.vue
<template>
	<div class="father">
        <p  @sonEvent="handlerSon"></p>
    </div>
</template>
<script>
    components:
    name: "Father"
    data:{
        
    },
methods:{
    handlerSon(sonData){
        console.log(sonData);
    }
}
</script>

// 子组件 Son.vue
<template>
	<div class="father">
        <p ref="son" @click="sonEvent" v-model:"sonData"></p>
    </div>
</template>
methods:{
    sonEvent(){
        this.refs.son.$emit(sonEvent, sonData)
    }
```

## 调用子组件方法

- ``ref`` and ``refs``

