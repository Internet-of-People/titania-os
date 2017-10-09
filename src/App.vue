<template>
  <div id="app">
    <img src="./assets/images/titania-logo.png">
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
@import './assets/css/titania.css'
</style>
