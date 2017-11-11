<template>
  <div class="dashboard-wrapper">
    <div class="display-flex">
      <dashboardCard v-for="serie in series" :key="serie[0]" :test-prop="serie"></dashboardCard>
    </div>
    <div>
      <div class="col-12">
        <div class="float-left chart-caption sans-serif-bold">CPU USAGE</div>
        <div class="float-right chart-caption time-picker">Last Month   &#9662;</div>
      </div>
      <div class="display-inline-flex">
        <highcharts class="chart" :options="options" ref="highcharts"></highcharts>
        <div class="legend-series">
          <div class="large-fontsize">dApps</div>
          <div class=""><span class="legend-1 padding-right-4">&#9679;</span>LOC Server</div>
          <div><span class="legend-2 padding-right-4">&#9679;</span>Profile Server</div>
          <div><span class="legend-3 padding-right-4">&#9679;</span>IPFS Lookup</div>
          <div><span class="legend-4 padding-right-4">&#9679;</span>IoP Wallet</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import dashboardCard from '@/components/dashboard/dashboardCard'

export default {
  name: 'dashboardMainContent',
  computed: {
    series: {
      get: function () {
        return this.$store.state.series
      }
    }
  },
  data: function () {
    return {
      options: {
        title: {
          text: ''
        },
        xAxis: {
          type: 'datetime',
          title: {
            text: ''
          }
        },
        yAxis: {
          title: {
            text: 'Percentage'
          },
          plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
          }]
        },
        legend: {
          enabled: false
        },
        exporting: {
          enabled: false
        },
        credits: {
          enabled: false
        },
        plotOptions: {
          spline: {
            marker: {
              enabled: true
            }
          }
        },
        series: [{
          name: 'LOC Server',
          data: [
            [Date.UTC(2017, 9, 1), 0],
            [Date.UTC(2017, 9, 4), 0.28],
            [Date.UTC(2017, 9, 6), 0.25],
            [Date.UTC(2017, 9, 7), 0.2],
            [Date.UTC(2017, 9, 12), 0.28],
            [Date.UTC(2017, 9, 16), 0.28],
            [Date.UTC(2017, 9, 20), 0.47],
            [Date.UTC(2017, 9, 21), 0.79],
            [Date.UTC(2017, 9, 26), 0.72],
            [Date.UTC(2017, 9, 30), 1.02]
          ],
          color: '#3366cc',
          marker: {
            symbol: 'circle',
            radius: 1
          }
        }, {
          name: 'Profile Server',
          data: [
            [Date.UTC(2017, 9, 1), 0],
            [Date.UTC(2017, 9, 3), 0.25],
            [Date.UTC(2017, 9, 5), 1.41],
            [Date.UTC(2017, 9, 7), 1.64],
            [Date.UTC(2017, 9, 8), 1.6],
            [Date.UTC(2017, 9, 12), 2.55],
            [Date.UTC(2017, 9, 13), 2.62],
            [Date.UTC(2017, 9, 17), 2.5],
            [Date.UTC(2017, 9, 19), 2.42],
            [Date.UTC(2017, 9, 20), 2.74],
            [Date.UTC(2017, 9, 21), 2.62],
            [Date.UTC(2017, 9, 21), 2.6],
            [Date.UTC(2017, 9, 22), 2.81],
            [Date.UTC(2017, 9, 23), 2.63],
            [Date.UTC(2017, 9, 30), 2.77]],
          color: '#dc3912',
          marker: {
            symbol: 'circle',
            radius: 1
          }
        }, {
          name: 'IPFS Service',
          data: [
            [Date.UTC(2017, 9, 1), 3.25],
            [Date.UTC(2017, 9, 7), 1.66],
            [Date.UTC(2017, 9, 8), 1.8],
            [Date.UTC(2017, 9, 9), 1.76],
            [Date.UTC(2017, 9, 11), 2.62],
            [Date.UTC(2017, 9, 12), 2.41],
            [Date.UTC(2017, 9, 12), 2.05],
            [Date.UTC(2017, 9, 14), 1.7],
            [Date.UTC(2017, 9, 24), 1.1],
            [Date.UTC(2017, 9, 27), 0]
          ],
          color: '#ff9900',
          marker: {
            symbol: 'circle',
            radius: 1
          }
        }, {
          name: 'IoP Wallet',
          data: [
            [Date.UTC(2017, 9, 2), 0],
            [Date.UTC(2017, 9, 6), 0.25],
            [Date.UTC(2017, 9, 9), 1.41],
            [Date.UTC(2017, 9, 15), 1.64],
            [Date.UTC(2017, 9, 24), 1.6],
            [Date.UTC(2017, 9, 28), 2.55],
            [Date.UTC(2017, 9, 30), 2.81]
          ],
          color: '#109618',
          marker: {
            symbol: 'circle',
            radius: 1
          }
        }]
      }
    }
  },
  components: {
    dashboardCard
  }
}
</script>
