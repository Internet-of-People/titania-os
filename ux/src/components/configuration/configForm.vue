<template>
    <div class="float-left center-aligned-slider outline-none">
      <div v-if="getOnSettingPage()" class="padding-20">
            <input id="boxname" name="boxname" v-model="configdetails.boxname" placeholder="MyTitaniumBox" class="sans-serif-normal box-name-field outline-none header-fontsize" type="text" maxLength="64" />
      </div>
      <div class="center-aligned-slider-body">
        <div class='config-slab '>
          <div class='display-inline-block'>
            <span id="config" @click="setTab('config')" v-if="showThisTab('user')" v-bind:class="{selectedConfigTab: currenttab === 'config'}" class="config-headers">USER</span>
            <span id="wireless" @click="setTab('wifi')" v-if="this.$store.state.wifi_support && showThisTab('wifi')" v-bind:class="{selectedConfigTab: currenttab === 'wifi'}" class="config-headers">WIFI</span>
          </div>
          <div v-if="currenttab === 'config' && showThisTab('user')" class='margin-top-20'>
            <div class="form-field-block col-12">
              <div class="sans-serif-normal text-align large-fontsize">Username</div>
              <input id="username" v-model="configdetails.username" class="config-input-field regular-fontsize" type="text" />
            </div>
            <div class="form-field-block col-12">
              <div class="sans-serif-normal text-align large-fontsize">Password</div>
              <input id="password" v-model="configdetails.password" class="config-input-field regular-fontsize" type="password" />
            </div>
            <div class="form-field-block col-12">
              <div class="sans-serif-normal text-align large-fontsize">Confirm Password</div>
              <input id="confirmPassword" v-model="configdetails.confirmPassword" class="config-input-field regular-fontsize" type="password" />
            </div>
          </div>
          <div v-else-if="this.$store.state.wifi_support && showThisTab('wifi')" class='margin-top-20'>
            <div class="form-field-block col-12">
              <div class="sans-serif-normal text-align large-fontsize">WIFI Network</div>
              <div class="text-align cursor-pointer selected-wifi" @click="getWiFiList()">{{currentwifiap}} <div v-if="this.editProp === false" class='float-right'>&#9662;</div></div>       
              <ul class='dropdown-config hide' >
                <li v-for="(item,index) in wifiAps" :key="index" v-if="item[0].length > 0" class="float-left  cursor-pointer col-11 selected" @click="setWifiAP(item[0])" >
                  <span v-if="item[0] == currentwifiap && item[0].length > 0" class="float-left cursor-pointer sans-serif-bold overflow-hidden" style="width: 100%;">{{item[0]}}</span>
                  <span v-else class="float-left cursor-pointer sans-serif-normal overflow-hidden" style="width:70%;">{{item[0]}}</span>
                </li>
              </ul>
            </div>
            <div class="form-field-block col-12">
              <div class="sans-serif-normal text-align large-fontsize">Security Protocol</div>
              <div class="text-align cursor-pointer selected-wifi" @click="getSecurityModeList()">{{currentprotocol}} <div v-if="this.editProp === false" class='float-right'>&#9662;</div></div>       
              <ul class='dropdown-encyption hide' >
                <li v-for="(item,index) in encryptModes" :key="index" v-if="item[0].length > 0" class="float-left  cursor-pointer col-11 selected" @click="setSecurityOptions(item)" >
                  <span v-if="item == currentprotocol" class="float-left cursor-pointer sans-serif-bold overflow-hidden" style="width: 100%;">{{item}}</span>
                  <span v-else class="float-left cursor-pointer sans-serif-normal overflow-hidden" style="width:70%;">{{item}}</span>
                </li>
              </ul>
            </div>
            <div class="form-field-block col-12">
              <div class="sans-serif-normal text-align large-fontsize">Password</div>
              <input id="wifipassword" v-model="configdetails.wifi_password" class="config-input-field regular-fontsize" type="password" />
            </div>
            <!-- <button id="" class="test-conn outline-none cursor-pointer outline-none sans-serif-normal small-fontsize">TEST</button> -->
          </div>
        </div>
      </div>
      <div class="col-12">
        <button id='saveForm' @click="saveConfig()" class="save-config button-primary float-right cursor-pointer outline-none large-fontsize">SAVE</button>
      </div>
  </div>
</template>

<script>
import Vue from 'vue'
export default {
  name: 'configForm',
  props: ['testProp', 'editProp', 'editWifiapProp'],
  computed: {
    wifiAps: {
      get: function () {
        return this.$store.state.configuration.wifi_aps
      }
    },
    encryptModes: {
      get: function () {
        return this.$store.state.encrypt_modes
      }
    },
    currenttab: {
      get: function () {
        return this.$store.state.configuration.tabname
      },
      set: function (newtab) {
        this.$store.state.configuration.tabname = newtab
      }
    },
    currentwifiap: {
      get: function () {
        if (this.editProp) {
          return this.editWifiapProp
        }
        return this.$store.state.configuration.wifi_aps_current
      },
      set: function (apname) {
        this.$store.state.configuration.wifi_aps_current = apname
      }
    },
    currentprotocol: {
      get: function () {
        // if (this.editProp) {
        //   return this.editWifiapProp
        // }
        // console.log(this.$store.state.configuration)
        return this.$store.state.configuration.wifi_encrpt
      },
      set: function (encyptmode) {
        this.$store.state.configuration.wifi_encrpt = encyptmode
      }
    }
  },
  data () {
    return {
      configdetails: {
        boxname: 'titania',
        username: '',
        password: '',
        wifi_password: '',
        confirmPassword: ''
      }
    }
  },
  methods: {
    setWifiAP (apname) {
      this.currentwifiap = apname
      $('.dropdown-config').addClass('hide')
      $('.dropdown-encyption').addClass('hide')
    },
    setSecurityOptions (encyptmode) {
      this.currentprotocol = encyptmode
      $('.dropdown-config').addClass('hide')
      $('.dropdown-encyption').addClass('hide')
    },
    saveConfig () {
      if (this.testProp) {
        if (this.testProp === 'user') {
          if (this.configdetails.username.length === 0) {
            Vue.toast('Enter username', {
              id: 'my-toast',
              className: ['toast-warning'],
              horizontalPosition: 'right',
              verticalPosition: 'bottom',
              duration: 2000,
              mode: 'queue'
            })
            $('#username').addClass('error-hint')
          } else if ($.inArray(this.configdetails.username, this.$store.state.settings.users) !== -1) {
            Vue.toast('User with this name already exists', {
              id: 'my-toast',
              className: ['toast-warning'],
              horizontalPosition: 'right',
              verticalPosition: 'bottom',
              duration: 2000,
              mode: 'queue'
            })
            $('#username').addClass('error-hint')
          } else if (this.configdetails.password !== this.configdetails.confirmPassword || this.configdetails.password.length === 0) {
            $('#username').removeClass('error-hint')
            Vue.toast(this.configdetails.password.length > 0 ? 'Password mismatch' : 'Password not supplied', {
              id: 'my-toast',
              className: ['toast-warning'],
              horizontalPosition: 'right',
              verticalPosition: 'bottom',
              duration: 2000,
              mode: 'queue'
            })
            $('#password').addClass('error-hint')
            $('#confirmPassword').addClass('error-hint')
          } else {
            $('#password').removeClass('error-hint')
            $('#confirmPassword').removeClass('error-hint')
            $('body').css('cursor', 'progress')
            $('#saveForm').css('cursor', 'wait')
            this.$store.dispatch('addNewUser', this.configdetails)
          }
        } else {
          if (this.editProp) {
            this.configdetails.wifi_ap = this.editWifiapProp
            $('body').css('cursor', 'progress')
            $('#saveForm').css('cursor', 'wait')
            this.$store.dispatch('editWifi', this.configdetails)
          } else {
            this.configdetails.wifi_ap = this.currentwifiap
            $('body').css('cursor', 'progress')
            $('#saveForm').css('cursor', 'wait')
            this.$store.dispatch('addWifi', this.configdetails)
          }
        }
      } else {
        if (this.configdetails.boxname.length === 0) {
          Vue.toast('Enter box name', {
            id: 'my-toast',
            className: ['toast-warning'],
            horizontalPosition: 'right',
            verticalPosition: 'bottom',
            duration: 2000,
            mode: 'queue'
          })
          $('#boxname').addClass('error-hint')
        } else if (this.configdetails.username.length === 0) {
          $('#boxname').removeClass('error-hint')
          Vue.toast('Enter username', {
            id: 'my-toast',
            className: ['toast-warning'],
            horizontalPosition: 'right',
            verticalPosition: 'bottom',
            duration: 2000,
            mode: 'queue'
          })
          $('#username').addClass('error-hint')
        } else if (this.configdetails.password !== this.configdetails.confirmPassword || this.configdetails.password.length === 0) {
          $('#username').removeClass('error-hint')
          Vue.toast(this.configdetails.password.length > 0 ? 'Password mismatch' : 'Password not supplied', {
            id: 'my-toast',
            className: ['toast-warning'],
            horizontalPosition: 'right',
            verticalPosition: 'bottom',
            duration: 2000,
            mode: 'queue'
          })
          $('#password').addClass('error-hint')
          $('#confirmPassword').addClass('error-hint')
        } else {
          $('#password').removeClass('error-hint')
          $('#confirmPassword').removeClass('error-hint')
          this.configdetails.wifi_ap = this.currentwifiap
          // adding wait cursor
          $('body').css('cursor', 'progress')
          $('#saveForm').css('cursor', 'wait')
          this.$store.dispatch('saveConfigForm', this.configdetails)
        }
      }
    },
    getWiFiList () {
      if (this.editProp === true) {
        return
      }
      if ($('.dropdown-config.hide').length) {
        $('.dropdown-config').removeClass('hide')
      } else {
        $('.dropdown-config').addClass('hide')
      }
    },
    getSecurityModeList () {
      // if (this.editProp === true) {
      //   return
      // }
      if ($('.dropdown-encyption.hide').length) {
        $('.dropdown-encyption').removeClass('hide')
      } else {
        $('.dropdown-encyption').addClass('hide')
      }
    },
    setTab (tab) {
      this.currenttab = tab
    },
    getOnSettingPage () {
      return this.testProp === undefined
    },
    showThisTab (tabname) {
      if (tabname === 'wifi' && this.testProp === undefined && this.wifiAps.length === 0) {
        return false
      }
      return this.testProp === undefined || this.testProp === tabname
    }
  },
  mounted: function () {
    // omitted extra fetch aps call in case of user addition
    if (this.testProp !== 'user' && this.$store.state.wifi_support) {
      this.$store.dispatch('getAllAPs')
    }
  }
}
</script>
