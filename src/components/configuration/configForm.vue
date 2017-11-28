<template>
    <div class="float-left center-aligned-slider outline-none">
      <div class="padding-20">
            <input id="boxname" name="boxname" v-model="configdetails.boxname" placeholder="Enter box name" class="sans-serif-normal box-name-field outline-none header-fontsize" type="text" maxLength="64" />
      </div>
      <div class="center-aligned-slider-body">
        <div class='config-slab '>
          <span id="config" class="config-headers">CONFIG</span>
          <div class="form-field-block col-12">
             <div class="sans-serif-normal text-align large-fontsize">Username</div>
             <input v-model="configdetails.username" class="config-input-field regular-fontsize" type="text" />
          </div>
          <div class="form-field-block col-12">
             <div class="sans-serif-normal text-align large-fontsize">Password</div>
             <input v-model="configdetails.password" class="config-input-field regular-fontsize" type="password" />
          </div>
          <div class="form-field-block col-12">
             <div class="sans-serif-normal text-align large-fontsize">Confirm Password</div>
             <input v-model="configdetails.confirmPassword" class="config-input-field regular-fontsize" type="password" />
          </div>
        </div>
        <div class='config-slab'>
          <span id="wireless" class="config-headers">WIFI SETUP</span>
          <div class="form-field-block col-12">
            <div class="sans-serif-normal text-align regular-fontsize">WIFI Network</div>
            <div class="text-align cursor-pointer selected-wifi" @click="getWiFiList()">{{currentwifiap}} <div class='float-right'>&#9662;</div></div>       
             <ul class='dropdown-config hide' >
               <li v-for="item in wifiAps" :key="item" class="float-left  cursor-pointer col-12 selected" @click="setWifiAP(item)" >
                 <span v-if="item == currentwifiap" class="float-left cursor-pointer sans-serif-bold overflow-hidden" style="width: 100%;">{{item}}</span>
                 <span v-else class="float-left cursor-pointer sans-serif-normal overflow-hidden" style="width: 100%;">{{item}}</span>
               </li>
            </ul>
          </div>
          <div class="form-field-block col-12">
             <div class="sans-serif-normal text-align large-fontsize">Username (Optional)</div>
             <input class="config-input-field regular-fontsize" type="text" />
          </div>
          <div class="form-field-block col-12">
             <div class="sans-serif-normal text-align large-fontsize">Password</div>
             <input v-model="configdetails.wifi_password" class="config-input-field regular-fontsize" type="password" />
          </div>
          <!-- <button id="" class="test-conn outline-none cursor-pointer outline-none sans-serif-normal small-fontsize">TEST</button> -->
        </div>
      </div>
      <div class="col-12">
        <button @click="saveConfig()" class="save-config button-primary float-right cursor-pointer outline-none large-fontsize">SAVE</button>
      </div>
  </div>
</template>

<script>
import Vue from 'vue'
export default {
  props: [
    'closeConfigForm'
  ],
  name: 'configForm',
  computed: {
    wifiAps: {
      get: function () {
        return this.$store.state.configuration.wifi_aps
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
        return this.$store.state.configuration.wifi_aps_current
      },
      set: function (apname) {
        this.$store.state.configuration.wifi_aps_current = apname
      }
    }
  },
  data () {
    return {
      configdetails: {
        boxname: '',
        username: '',
        password: '',
        wifi_password: ''
      }
    }
  },
  methods: {
    setWifiAP (apname) {
      this.currentwifiap = apname
      $('.dropdown-config').addClass('hide')
    },
    saveConfig () {
      if (this.configdetails.boxname.length === 0) {
        Vue.toast('Enter box name', {
          id: 'my-toast',
          className: ['toast-warning'],
          horizontalPosition: 'right',
          verticalPosition: 'bottom',
          duration: 2000,
          mode: 'queue'
        })
        return
      } else if (this.configdetails.username.length === 0) {
        Vue.toast('Enter username', {
          id: 'my-toast',
          className: ['toast-warning'],
          horizontalPosition: 'right',
          verticalPosition: 'bottom',
          duration: 2000,
          mode: 'queue'
        })
        return
      }
      this.configdetails.wifi_ap = this.currentwifiap
      this.$store.dispatch('saveConfigForm', this.configdetails)
    },
    getWiFiList () {
      if ($('.dropdown-config.hide').length) {
        $('.dropdown-config').removeClass('hide')
      } else {
        $('.dropdown-config').addClass('hide')
      }
    }
  }
}
</script>
