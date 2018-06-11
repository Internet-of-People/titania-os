<template>
    <div>
        <sidebarParent></sidebarParent>
        <headerParent :name-prop="page"></headerParent>
        <pageLoader v-if="if_loading"></pageLoader>
        <dappsHubContent v-if="!if_loading" :load-apps="!if_loading"/>
    </div>
</template>

<script>
import sidebarParent from '@/components/common/sidebarParent'
import headerParent from '@/components/common/headerParent'
import pageLoader from '@/components/common/pageLoader'
import dappsHubContent from '@/components/dappshub/dappsHubContent'

var refreshtimeout = null

export default {
  name: 'dappshub',
  computed: {
    page () {
      return 'DAPPS HUB'
    },
    if_loading: {
      get: function () {
        return this.$store.state.dappsjson.length == 0
      }     
    }
  },
  components: {
    sidebarParent,
    headerParent,
    pageLoader,
    dappsHubContent
  },
  methods: {
    onMount: function () {
      if (this.$route.params.setSession) {
        this.$session.start()
        this.$store.dispatch('fetchAlldApps')
        this.$store.state.currentPage = 'dappshub'
      } else if (!this.$session.exists()) {
        this.$router.push('/login')
        this.$store.state.currentPage = 'login'
      } else {
        this.$store.dispatch('fetchAlldApps')
        this.$store.state.currentPage = 'dappshub'
      }
    }
  },
  mounted: function () {
    this.onMount()
  },
  updated: function () {
    var that = this
    refreshtimeout = setTimeout(function(){
      that.onMount()
    } , 60000)  
  },
  destroyed: function () {
    clearTimeout(refreshtimeout)
  }
}
</script>
