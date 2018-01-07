<template>
  <div class='col-12 settings-page'>
    <div class='col-12 settings-container'>
        <div class='settings-header'>WiFi LIST</div> 
        <div v-for="wifi in wifiaps" v-if="wifi.length > 0" :key="wifi" class='user-row'> 
            <div class='col-10'>{{wifi}}</div>
            <div class='col-1 float-right cursor-pointer' @click="updatewifi(wifi)" title="Update connection">
                <img class="edit-remove-icon" src="../../assets/images/edit.svg"/>
            </div>
            <div class='col-1 float-right del-wifi cursor-pointer' @click="deletewifi(wifi)" title="Delete connection">
                <img class="edit-remove-icon" src="../../assets/images/trash.svg"/>
            </div>
        </div>
        <div class='cursor-pointer float-left add-new display-inline-flex' @click="addNewWifi()">
            <img class='margin-right-8' src="../../assets/images/icon-plus.svg">
            <div>Add new WiFi</div>
        </div>
    </div>
    <div v-if="configure">
      <config-form :test-prop='tabname' :edit-prop='iseditwifi' :edit-wifiap-prop='editwifiname' ref="configFormDiv" />
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
    },
    iseditwifi: {
      get: function () {
        return this.$store.state.settings.getaseditwifiform
      },
      set: function (val) {
        this.$store.state.settings.getaseditwifiform = val
      }
    },
    editwifiname: {
      get: function () {
        return this.$store.state.settings.editwifiap
      },
      set: function (val) {
        this.$store.state.settings.editwifiap = val
      }
    }
  },
  methods: {
    updatewifi: function (wifiap) {
      this.iseditwifi = true
      this.editwifiname = wifiap
      this.configure = !this.configure
    },
    deletewifi: function (wifiap) {
      var deleterequest = {}
      deleterequest.wifi = wifiap
      // add wait cursor
      $('body').css('cursor', 'progress')
      $('.del-wifi').css('cursor', 'wait')
      this.$store.dispatch('deleteWifi', deleterequest)
    },
    addNewWifi: function () {
      if (this.$store.state.configuration.wifi_aps.length === 0) {
        Vue.toast('No WiFi APs found nearby', {
          id: 'my-toast',
          className: ['toast-warning'],
          horizontalPosition: 'right',
          verticalPosition: 'bottom',
          duration: 4000,
          mode: 'queue',
          transition: 'my-transition'
        })
        return
      }
      this.iseditwifi = false
      this.editwifiname = ''
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
