<template>
  <div @keyup.enter="configure()">
    <div>
      <img class="logo-icon-config" src="../../assets/images/titania-Logo-port.svg">
      <div class='config-help'>Welcome aboard</div>
    </div>
    <button type="button" @click="configure()" class="outline-none large-fontsize button-primary" id="login_submit">CONFIGURE</button>
    <div v-if="enableConfigure">
      <config-form :closeConfigForm="closeForm" />
      <div class="fadeout" @click="closeForm()"></div>
    </div>
  </div>
</template>

<script>
import configForm from '@/components/configuration/configForm'
export default {
  name: 'configure',
  components: { configForm },
  computed: {
    enableConfigure () {
      return this.$store.state.configuration.enableConfigure
    }
  },
  methods: {
    configure () {
      this.$store.dispatch('toggleConfigForm')
    },
    closeForm () {
      this.$store.dispatch('toggleConfigForm')
    }
  },
  mounted: function () {
    this.$store.dispatch('getAllAPs')
  }
}
</script>
