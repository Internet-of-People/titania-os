<template>
  <div id='container' @keyup.enter.native="submit">
    <div>
      <img class="logo-icon-config" src="../../assets/images/titania-Logo-port.svg">
    </div>
    <button type="button" @click="reboot()" class="outline-none large-fontsize button-primary" id="restart_submit">RESTART</button>
  </div>
</template>

<script>
export default {
  name: 'restart',
  methods: {
    reboot () {
        this.$store.dispatch('rebootSystem')
    }
  },
  created: function () {
    window.addEventListener('keyup', this.submit)
    this.$store.dispatch('getCreds')
  },
  unmounted: function () {
    window.removeEventListener('keyup', this.submit)
  }
}
</script>
