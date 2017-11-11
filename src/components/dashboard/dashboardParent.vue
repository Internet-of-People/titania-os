<template>
  <div>
    <sidebarParent></sidebarParent>
    <headerParent></headerParent>
    <div class="margin-20">
      <dashboardMainContent></dashboardMainContent>
    </div>
  </div>
</template>

<script>
import sidebarParent from '@/components/dashboard/sidebarParent'
import headerParent from '@/components/dashboard/headerParent'
import dashboardMainContent from '@/components/dashboard/dashboardMainContent'

export default {
  name: 'dashboard',
  components: {
    sidebarParent,
    headerParent,
    dashboardMainContent
  },
  mounted: function () {
    if (this.$route.params.setSession) {
      this.$session.start()
      this.$store.dispatch('getDashboardCards')
    } else if (!this.$session.exists()) {
      this.$router.push('/login')
    } else {
      this.$store.dispatch('getDashboardCards')
    }
  }
}
</script>
