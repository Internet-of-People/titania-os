<template>
  <div>
    <sidebarParent></sidebarParent>
    <headerParent :name-prop="page"></headerParent>
    <div class="margin-20">
      <dappsMainContent></dappsMainContent>
    </div>
  </div>
</template>

<script>
import sidebarParent from '@/components/sidebarParent'
import headerParent from '@/components/headerParent'
import dappsMainContent from '@/components/dappsconsole/dappsMainContent'

export default {
  name: 'dashboard',
  computed: {
    page () {
      return 'DAPPS CONSOLE'
    }
  },
  components: {
    sidebarParent,
    headerParent,
    dappsMainContent
  },
  mounted: function () {
    if (this.$route.params.setSession) {
      this.$session.start()
      this.$store.dispatch('getDashboardCards')
      this.$store.dispatch('getDashboardChart')
    } else if (!this.$session.exists()) {
      this.$router.push('/login')
    } else {
      this.$store.dispatch('getDashboardCards')
      this.$store.dispatch('getDashboardChart')
    }
  }
}
</script>
