<template>
  <div>
    <sidebarParent></sidebarParent>
    <headerParent :name-prop="page"></headerParent>
    <div class="margin-20">
      <div>
        <containerMainContent></containerMainContent>
      </div>
    </div>
  </div>
</template>

<script>
import sidebarParent from '@/components/sidebarParent'
import headerParent from '@/components/headerParent'
import containerMainContent from '@/components/containerstats/containerMainContent.vue'

export default {
  name: 'dashboard',
  computed: {
    page () {
      return 'DOCKER METRICS'
    }
  },
  components: {
    sidebarParent,
    headerParent,
    containerMainContent
  },
  mounted: function () {
    if (this.$route.params.setSession) {
      this.$session.start()
      this.$store.dispatch('getContainerStats')
    } else if (!this.$session.exists()) {
      this.$router.push('/login')
    } else {
      this.$store.dispatch('getContainerStats')
    }
  }
}
</script>
