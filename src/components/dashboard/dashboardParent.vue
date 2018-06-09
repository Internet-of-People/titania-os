<template>
  <div style="height:inherit;">
    <sidebarParent></sidebarParent>
    <headerParent :name-prop="page"></headerParent>
    <div class="margin-20">
      <dashboardMainContent v-if="this.$store.state.dashboardChart.series.length !== 0"></dashboardMainContent>
      <pageLoader v-if="this.$store.state.dashboardChart.series.length === 0"></pageLoader>
    </div>
  </div>
</template>

<script>
import sidebarParent from '@/components/common/sidebarParent'
import headerParent from '@/components/common/headerParent'
import dashboardMainContent from '@/components/dashboard/dashboardMainContent'
import pageLoader from '@/components/common/pageLoader'

var refreshtimeout = null

export default {
  name: 'dashboard',
  computed: {
    page () {
      return 'DASHBOARD'
    }
  },
  components: {
    sidebarParent,
    headerParent,
    dashboardMainContent,
    pageLoader
  },
  methods: {
    onMount: function () {
      if(this.$store.state.currentPage === 'dashboard'){
        if (this.$route.params.setSession && !this.$session.exists()) {
          this.$store.dispatch('getDashboardCards')
          this.$store.dispatch('getDashboardChart')
          this.$store.dispatch('getNatpmpStatus')
          this.$session.start()
        } else if (!this.$session.exists()) {
          this.$router.push('/login')
          this.$store.state.currentPage = 'login'
        } else {
          this.$store.dispatch('getDashboardCards')
          this.$store.dispatch('getDashboardChart')
        }
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
    } , 30000)  
  },
  destroyed: function () {
    clearTimeout(refreshtimeout)
  }
}
</script>
