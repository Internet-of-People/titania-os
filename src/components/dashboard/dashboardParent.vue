<template>
  <div>
    <sidebarParent></sidebarParent>
    <headerParent :name-prop="page"></headerParent>
    <div class="margin-20">
      <dashboardMainContent v-if="this.$store.state.dashboardChart.series.length != 0"></dashboardMainContent>
    </div>
  </div>
</template>

<script>
import sidebarParent from '@/components/common/sidebarParent'
import headerParent from '@/components/common/headerParent'
import dashboardMainContent from '@/components/dashboard/dashboardMainContent'

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
    dashboardMainContent
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
  }
}
</script>
