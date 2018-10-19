<template>
  <div class="dashboard-wrapper">
    <div class="display-flex">
      <dashboardCard v-for="serie in series" :key="serie[0]" :test-prop="serie"></dashboardCard>
    </div>
    <div class='some-class'>
      <div class="col-12">
        <div class="float-left chart-caption sans-serif-bold">CPU USAGE</div>
      </div>
      <div class="display-inline-flex">
        <highcharts class="chart" :options="options" ref="highcharts"></highcharts>
        <div class="legend-series">
          <div class="large-fontsize">dApps</div>
          <div class="legends">
            <div :id="serie" v-for="serie in seriesname" :title="serie" :key="serie" class='cursor-pointer' @click="toggleSeries(serie)"> 
             <span class="padding-left-4">&#9679;</span>
              {{serie}}
            </div>
          </div>
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
    },
    seriesname: {
      get: function () {
        return this.$store.state.dashboardChart.seriesname
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
        backgroundColor: null,
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
          data: [],
          color: '#3366cc',
          marker: {
            symbol: 'circle',
            radius: 1
          }
        }, {
          data: [],
          color: '#dc3912',
          marker: {
            symbol: 'circle',
            radius: 1
          }
        }, {
          data: [],
          color: '#ff9900',
          marker: {
            symbol: 'circle',
            radius: 1
          }
        }, {
          data: [],
          color: '#109618',
          marker: {
            symbol: 'circle',
            radius: 1
          }
        }, {
          data: [],
          color: '#9400D3',
          marker: {
            symbol: 'circle',
            radius: 1
          }
        }]
      }
    }
  },
  methods: {
    updateCredits: function () {
      var chart = this.$refs.highcharts.chart
      var series = this.$store.state.dashboardChart.series
      var seriesname = this.$store.state.dashboardChart.seriesname
      for (var i = 0; i < series.length; i++) {
        if (chart) {
          chart.series[i].update({name: seriesname[i]}, false)
          chart.series[i].setData(series[i])
        }
      }
    },
    toggleSeries: function (seriesVal) {
      var chart = this.$refs.highcharts.chart
      var pos
      var series = this.$store.state.dashboardChart.series
      var seriesname = this.$store.state.dashboardChart.seriesname
      var elem = seriesVal
      pos = seriesname.indexOf(seriesVal)
      if (chart.series[pos].yData.length === 0) {
        $('#' + elem).removeClass('fadeout-row')
        chart.series[pos].setData(series[pos])
      } else {
        $('#' + elem).addClass('fadeout-row')
        chart.series[pos].setData([])
      }
    }
  },
  mounted: function () {
   this.updateCredits()
  },
  components: {
    dashboardCard
  }
}
</script>
