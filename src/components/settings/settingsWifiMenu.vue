<template>
  <div class='col-12 settings-page'>
    <div class='col-12 settings-container'>
        <div class='settings-header'>WiFi LIST</div> 
        <div v-for="wifi in wifiaps" v-if="wifi.length > 0" :key="wifi" class='user-row'> 
            <div class='col-10'>{{wifi}}</div>
            <div class='col-1 float-right cursor-pointer' @click="updatewifi(wifi)" title="Update connection">
                <img class="edit-remove-icon" src="../../assets/images/edit.svg"/>
            </div>
            <div class='col-1 float-right cursor-pointer' @click="deletewifi(wifi)" title="Delete connection">
                <img class="edit-remove-icon" src="../../assets/images/trash.svg"/>
            </div>
        </div>
        <div class='cursor-pointer float-left add-new display-inline-flex' @click="addNewWifi()">
            <img class='margin-right-8' src="../../assets/images/icon-plus.svg">
            <div>Add new WiFi</div>
        </div>
    </div>
    <div v-if="configure">
      <config-form :test-prop='tabname' ref="configFormDiv" />
      <div class="fadeout" @click="toggleConfig()"></div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import VueLocalStorage from 'vue-ls'
import configForm from '@/components/configuration/configForm'
Vue.use(VueLocalStorage)

export default {
  name: 'wifilist',
  components: {
    configForm
  },
  computed: {
    wifiaps: {
      get: function () {
        return this.$store.state.settings.wifi
      }
    },
    configure: {
      get: function () {
        return this.$store.state.settings.getform
      },
      set: function (value) {
        this.$store.state.settings.getform = value
      }
    },
    tabname: {
      get: function () {
        return 'wifi'
      }
    }
  },
  methods: {
    updatewifi: function (wifiap) {
      console.log(wifiap)
      var updaterequest = {}
      updaterequest.wifi = wifiap
      this.$store.dispatch('updateWiFi', updaterequest)
    },
    deletewifi: function (wifiap) {
      console.log(wifiap)
      var deleterequest = {}
      deleterequest.wifi = wifiap
      this.$store.dispatch('deleteWifi', deleterequest)
    },
    addNewWifi: function () {
      this.configure = !this.configure
    },
    toggleConfig: function () {
      this.addNewWifi()
    },
    submit: function (event) {
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
  unmounted: function () {
    window.removeEventListener('keyup', this.submit)
  }
}
</script>
