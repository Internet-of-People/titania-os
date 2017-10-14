<template>
  <div @keyup.enter="configure()">
    <div>
      <img src="../../assets/images/titania-logo.png">
      <h1>Welcome aboard, Titania</h1>
    </div>
    <button type="button" @click="configure()" class="outline-none small-fontsize button-primary" id="login_submit">CONFIGURE</button>
    <div v-if="enableConfigure">
      <config-form :closeConfigForm="closeForm" />
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
      this.$store.commit('openConfigForm')
    },
    closeForm () {
      this.$store.commit('closeConfigForm')
    }
  }
}
</script>
