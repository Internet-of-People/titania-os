<template>
  <div id="app">
    <router-view/>
    <footer-parent/>
  </div>
</template>

<script>
import footerParent from '@/components/common/footerParent'
export default {
  components: { footerParent },
  name: 'app'
}
</script>

<style>
@import './assets/css/titania.css'
</style>
