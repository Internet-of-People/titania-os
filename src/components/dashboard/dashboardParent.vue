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
  mounted: function () {
    if (this.$route.params.setSession && !this.$session.exists()) {
      this.$store.dispatch('getDashboardCards')
      this.$store.dispatch('getDashboardChart')
      this.$session.start()
    } else if (!this.$session.exists()) {
      this.$router.push('/login')
      this.$store.state.currentPage = 'login'
    } else {
      this.$store.dispatch('getDashboardCards')
      this.$store.dispatch('getDashboardChart')
    }
  },
  updated: function () {
    var that = this
    setTimeout(function(){
      if (that.$route.params.setSession && !that.$session.exists()) {
        that.$store.dispatch('getDashboardCards')
        that.$store.dispatch('getDashboardChart')
        that.$session.start()
      } else if (!that.$session.exists()) {
        that.$router.push('/login')
        that.$store.state.currentPage = 'login'
      } else {
        that.$store.dispatch('getDashboardCards')
        that.$store.dispatch('getDashboardChart')
      }
    } , 30000)  
  }
}
</script>
