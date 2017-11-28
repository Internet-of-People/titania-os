<div class='sidebar-container dark-black'>
</div>

<template>
  <div class='sidebar-container dark-black'>
    <div @click="tabSwitch('')" title='Dashboard'>
      <img class="logo-icon-small cursor-pointer" src="../assets/images/titania-logo-clean.svg">
    </div>
    <div class='margin-top-20 cursor-pointer' title='dApps Console' @click="tabSwitch('dappsconsole')" v-bind:class="{ activeDrilldown: currentTab('dappsconsole')}">
      <img class="tab-label" src="../assets/images/dApps-icon.svg">
    </div>
    <div @click="tabSwitch('stats')" title='dApps Stats' class='cursor-pointer' v-bind:class="{ activeDrilldown: currentTab('stats')}">
      <img class="tab-label" src="../assets/images/uptime-icon.svg">
    </div>
    <div @click="tabSwitch('threads')" title='Threads' class='cursor-pointer' v-bind:class="{ activeDrilldown: currentTab('threads')}">
      <img class="tab-label" src="../assets/images/thread-icon.svg">
    </div>
  </div>
</template>

<script>
import router from '../router'

export default {
  name: 'sidebarParent',
  computed: {
    currentPage: {
      get () {
        return this.$store.state.currentPage
      }
    }
  },
  methods: {
    tabSwitch (tabname) {
      if (tabname.length === 0) {
        router.push('/')
        this.$store.dispatch('switchDrilldown', 'dashboard')
      } else {
        router.push('/' + tabname)
        this.$store.dispatch('switchDrilldown', tabname)
      }
    },
    currentTab (tabname) {
      return this.currentPage === tabname
    }
  }
}
</script>
