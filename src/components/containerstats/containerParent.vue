<template>
  <div>
    <sidebarParent></sidebarParent>
    <headerParent :name-prop="page"></headerParent>
    <div class="stats-page">
      <div>
        <containerMainContent></containerMainContent>
      </div>
    </div>
    <pageLoader v-if="this.$store.state.dockerstats.length === 0"></pageLoader>
  </div>
</template>

<script>
import sidebarParent from '@/components/common/sidebarParent'
import headerParent from '@/components/common/headerParent'
import containerMainContent from '@/components/containerstats/containerMainContent.vue'
import pageLoader from '@/components/common/pageLoader'

export default {
  name: 'containerstats',
  computed: {
    page () {
      return 'DOCKER METRICS'
    }
  },
  components: {
    sidebarParent,
    headerParent,
    containerMainContent,
    pageLoader
  },
  mounted: function () {
    if (this.$route.params.setSession) {
      this.$session.start()
      this.$store.dispatch('getContainerStats')
      this.$store.state.currentPage = 'stats'
    } else if (!this.$session.exists()) {
      this.$router.push('/login')
      this.$store.state.currentPage = 'login'
    } else {
      this.$store.dispatch('getContainerStats')
      this.$store.state.currentPage = 'stats'
    }
  },
  updated: function() {
    var that = this
    setTimeout(function(){
      that.$store.dispatch('getContainerStats')
    }, 10000)
  }
}
</script>
