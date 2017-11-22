<template>
  <div>
    <sidebarParent></sidebarParent>
    <headerParent :name-prop="page"></headerParent>
    <div class="margin-20">
    </div>
  </div>
</template>

<script>
import sidebarParent from '@/components/sidebarParent'
import headerParent from '@/components/headerParent'

export default {
  name: 'threads',
  computed: {
    page () {
      return 'THREADS'
    }
  },
  components: {
    sidebarParent,
    headerParent
  },
  mounted: function () {
    if (!this.$session.exists()) {
      this.$router.push('/login')
    } else {
      this.$store.dispatch('getThreads')
    }
  }
}
</script>
