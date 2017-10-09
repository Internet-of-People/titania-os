<template>
  <div id="app">
    <img src="./assets/titania-logo.png">
    <router-view/>
    <footer-parent/>
  </div>
</template>

<script>
import footerParent from '@/components/footerParent'
export default {
  components: { footerParent },
  name: 'app'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
