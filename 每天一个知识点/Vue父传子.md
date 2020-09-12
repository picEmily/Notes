# 项目结构

components

	- Parent.vue
	- Child.vue

App.vue

# 代码

Parent.vue


```html
<template>
  <div>
    <Child v-bind:msg="parentMsg"></Child>  
  <div>
</template>
  
<script>
import Child from "@/comoponent/Child"  
export default {
  name: "Parent",			// the name of this component
  component:{ Child }	// sub components this component contains,
  data() {						// data must be a fn
    return() {
      parentMsg: "Hola mi hijo"
    }
  }，
  methods:{
    //...
  }
}
</script>
<style scoped></style>
```

Child.vue

```html
<template>
  <div class="child">
    {{ msg }}  
  <div>
</template>
  
<script>
export default {
  name: "Child",	// the name of this component
  data() {
    // data must be a fn
    return() {
    }
  }，
  methods:{
    //...
  },
  props{
    // 父传子 传到这了
    msg: String
  }
}
</script>
<style scoped></style>
```

