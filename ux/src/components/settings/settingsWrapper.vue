<template>
  <div class=''>
    <div class='float-left display-inline-flex col-12 settings-options'>
        <div @click="setSettingsOption('users')" v-bind:class="{highlightedOption: getSelected('users')}">USERS</div>
        <div v-if="this.$store.state.wifi_support" @click="setSettingsOption('wifi')" v-bind:class="{highlightedOption: getSelected('wifi')}">WIFI</div>
    </div>
    <userlist v-if="getSelected('users')" ></userlist>
    <wifilist v-if="this.$store.state.wifi_support && getSelected('wifi')"></wifilist>
  </div>
</template>

<script>

import containerChart from '@/components/settings/settingsWrapper'
import userlist from '@/components/settings/settingsUserMenu'
import wifilist from '@/components/settings/settingsWifiMenu'

export default {
  name: 'settingsWrapper',
  components: {
    containerChart,
    userlist,
    wifilist
  },
  computed: {
    settingOption: {
      get: function () {
        return this.$store.state.settingOption
      },
      set: function (option) {
        this.$store.state.settingOption = option
      }
    }
  },
  methods: {
    getSelected: function (option) {
      return this.settingOption === option
    },
    setSettingsOption: function (option) {
      this.settingOption = option
    }
  },
  updated () {
    if (!this.$store.state.wifi_support) {
      this.settingOption = 'users'
    }
  }
}
</script>
