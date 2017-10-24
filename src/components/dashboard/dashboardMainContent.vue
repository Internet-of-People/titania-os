<template>
  <div class="display-flex">
    <dashboardCard v-for="serie in series" :key="serie.drilldownname" :test-prop="serie"></dashboardCard>
  </div>
</template>

<script>
import dashboardCard from '@/components/dashboard/dashboardCard'
export default {
  name: 'dashboardMainContent',
  data: function () {
    return {
      series: [
        { drilldownname: 'Total Apps Running',
          caption: 'Show all apps',
          count: 3 },
        { drilldownname: 'Uptime',
          caption: 'Show average uptime',
          count: '1 hour' },
        { drilldownname: 'Neighboring Nodes',
          caption: 'Show neighboring nodes',
          count: 3 },
        { drilldownname: 'Threads',
          caption: 'Show all threads',
          count: '2.3K' }
      ]
    }
  },
  components: {
    dashboardCard
  }
}
</script>
