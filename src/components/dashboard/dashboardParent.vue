<template>
  <div>
    <sidebarParent></sidebarParent>
    <headerParent :name-prop="page"></headerParent>
    <div class="margin-20">
      <dashboardMainContent></dashboardMainContent>
    </div>
  </div>
</template>

<script>
import sidebarParent from '@/components/sidebarParent'
import headerParent from '@/components/headerParent'
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
    if (this.$route.params.setSession) {
      this.$session.start()
      this.$store.dispatch('getDashboardCards')
      this.$store.dispatch('getDashboardChart')
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
