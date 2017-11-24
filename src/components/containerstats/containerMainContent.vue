<template>
  <div class='display-flex'>
      <!-- <containerChart v-for="stats in dockerstats" class='display-flex' 
        :test-prop="stats" :key="stats.container_name">
      </containerChart> -->
      <containerChart class=''
        :test-prop="dockerstats[0]" :key="dockerstats[0].container_name">
      </containerChart>
  </div>
</template>

<script>

import containerChart from '@/components/containerstats/containerChart'
export default {
  name: 'dappsMainContent',
  components: {
    containerChart
  },
  computed: {
    dockerstats: {
      get: function () {
        return this.$store.state.dockerstats
      }
    }
  }
}
</script>
