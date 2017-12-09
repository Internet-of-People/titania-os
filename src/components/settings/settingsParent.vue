<template>
  <div>
    <sidebarParent></sidebarParent>
    <headerParent :name-prop="page"></headerParent>
    <div class="margin-20 display-table">
        <settingsWrapper></settingsWrapper>
    </div>
  </div>
</template>

<script>
import sidebarParent from '@/components/sidebarParent'
import headerParent from '@/components/headerParent'
import settingsWrapper from '@/components/settings/settingsWrapper'

export default {
  name: 'settings',
  computed: {
    page () {
      return 'SETTINGS'
    }
  },
  components: {
    sidebarParent,
    headerParent,
    settingsWrapper
  },
  mounted: function () {
    if (this.$route.params.setSession && !this.$session.exists()) {
      this.$store.dispatch('getSettingsList')
      this.$session.start()
    } else if (!this.$session.exists()) {
      this.$router.push('/login')
      this.$store.state.currentPage = 'login'
    } else {
      this.$store.dispatch('getSettingsList')
    //   this.$store.dispatch('getDashboardChart')
    }
  }
}
</script>
