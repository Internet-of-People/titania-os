<template>
  <div id='container' @keyup.enter.native="submit">
    <div>
      <img class="logo-icon-config" src="../../assets/images/titania-Logo-port.svg">
      <div class='config-help'>Welcome aboard</div>
    </div>
    <button type="button" @click="toggleConfig()" class="outline-none large-fontsize button-primary" id="login_submit">CONFIGURE</button>
    <div v-if="configure">
      <config-form ref="configFormDiv" />
      <div class="fadeout" @click="toggleConfig()"></div>
    </div>
  </div>
</template>

<script>
import configForm from '@/components/configuration/configForm'
export default {
  name: 'configure',
  components: { configForm },
  computed: {
    configure: {
      get: function () {
        return this.$store.state.configuration.enableConfigure
      },
      set: function (formstate) {
        this.$store.state.configuration.enableConfigure = formstate
      }
    }
  },
  methods: {
    toggleConfig () {
      this.configure = !this.configure
      // reseting form on close/exit
      if (!this.configure) {
        this.$store.state.configuration.tabname = 'config'
      }
    },
    submit (event) {
      if (event.which === 13) {
        // on enter press
        if ($('.center-aligned-slider').length === 0) {
          this.toggleConfig()
        } else {
          this.$refs.configFormDiv.saveConfig()
        }
      } else if (event.which === 27 && $('.center-aligned-slider').length === 1) {
        this.toggleConfig() // on esc press
      }
    }
  },
  created: function () {
    window.addEventListener('keyup', this.submit)
  },
  mounted: function () {
    this.$store.dispatch('getAllAPs')
    this.$store.dispatch('initApp')
  },
  unmounted: function () {
    window.removeEventListener('keyup', this.submit)
  }
}
</script>
