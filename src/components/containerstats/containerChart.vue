<template>
<div class='display-inline-flex'>
      <div class='stats-header'>{{testProp.container_name}}</div>
      <div class='container-chart-wrapper'>
            <div class='container-holder'>CPU USAGE / MEM USAGE </div>
            <highcharts class='chart-new' :options="options" ref="highcharts"></highcharts>
            <div class='label-chart-area'>
              <div class='display-inline-flex metrics-labels cursor-default'>
                  <div class='hint-text'>Toggle series visibility</div>
                  <div>MAX</div>
                  <div>MIN</div>
                  <div>AVG</div>
              </div>
              <div v-for="legend in legends_perc" class='text-align-left' :key="legend">
                <div :id="legend" class='display-inline-flex label-div-chart cursor-pointer' v-on:click="toggleSeriesChart('perc',legend)">
                  <div class='legend-color margin-right-4'></div>
                  <div class='label-text-chart'>{{legend}}</div>
                  <div v-for="val in getMax(legend)"class='display-inline-flex metrics-labels' :key="val">
                    <div>{{val}}</div>
                  </div>
                </div>
              </div>
            </div>
      </div>
      <div class='container-chart-wrapper'>
            <div class='container-holder'>MEM USAGE / MEM USAGE LIMIT</div>
            <highcharts class='chart-new' :options="options" ref="highcharts_mem"></highcharts>
            <div class='label-chart-area'>
              <div class='display-inline-flex metrics-labels cursor-default'>
                  <div class='hint-text'>Toggle series visibility</div>
                  <div>MAX</div>
                  <div>MIN</div>
                  <div>AVG</div>
              </div>
              <div v-for="legend in legends_mem" class='text-align-left' :key="legend">
                <div :id="legend" class='display-inline-flex label-div-chart cursor-pointer' v-on:click="toggleSeriesChart('mem',legend)">
                  <div class='legend-color margin-right-4'></div>
                  <div class='label-text-chart'>{{legend}}</div>
                  <div v-for="val in getMaxMeM(legend)"class='display-inline-flex metrics-labels' :key="val">
                    <div>{{val}}</div>
                  </div>
                </div>
              </div>
            </div>
      </div>
      <div class='container-chart-wrapper'>
            <div class='container-holder'>NET IO / BLOCK IO</div>
            <highcharts class='chart-new' :options="options" ref="highcharts_io"></highcharts>
            <div class='label-chart-area'>
              <div class='display-inline-flex metrics-labels cursor-default'>
                  <div class='hint-text'>Toggle series visibility</div>
                  <div>MAX</div>
                  <div>MIN</div>
                  <div>AVG</div>
              </div>
              <div v-for="legend in legends_io" class='text-align-left' :key="legend">
                <div :id="legend" class='display-inline-flex label-div-chart cursor-pointer' v-on:click="toggleSeriesChart('io',legend)">
                  <div class='legend-color margin-right-4'></div>
                  <div class='label-text-chart'>{{legend}}</div>
                  <div v-for="val in getMaxIO(legend)"class='display-inline-flex metrics-labels' :key="val">
                    <div>{{val}}</div>
                  </div>
                </div>
              </div>
            </div>
      </div>
    </div>
</template>

<script>

export default {
  name: 'containerChart',
  props: ['testProp'],
  computed: {
    legends_perc: {
      get: function () {
        return ['CPU_USAGE', 'MEM_PERC']
      }
    },
    legends_io: {
      get: function () {
        return ['NET_IN', 'NET_OUT', 'BLOCK_IN', 'BLOCK_OUT']
      }
    },
    legends_mem: {
      get: function () {
        return ['MEM_USAGE', 'MEM_USAGE_LIMIT']
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
            text: ''
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
          data: [],
          color: '#3366cc',
          marker: {
            symbol: 'circle',
            radius: 1
          }
        }, {
          name: 'Profile Server',
          data: [],
          color: '#dc3912',
          marker: {
            symbol: 'circle',
            radius: 1
          }
        }, {
          name: 'IPFS Service',
          data: [],
          color: '#ff9900',
          marker: {
            symbol: 'circle',
            radius: 1
          }
        }, {
          name: 'IoP Wallet',
          data: [],
          color: '#109618',
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
      var series = this.$store.state.dockerstats[0].data_perc
      var seriesname = this.legends_perc
      for (var i = 0; i < series.length; i++) {
        chart.series[i].update({name: seriesname[i]}, false)
        chart.series[i].setData(series[i])
      }
      var chartIo = this.$refs.highcharts_io.chart
      series = this.$store.state.dockerstats[0].data_io
      seriesname = this.legends_io
      for (i = 0; i < series.length; i++) {
        chartIo.series[i].update({name: seriesname[i]}, false)
        chartIo.series[i].setData(series[i])
      }
      var chartMem = this.$refs.highcharts_mem.chart
      series = this.$store.state.dockerstats[0].data_mem
      seriesname = this.legends_io
      for (i = 0; i < series.length; i++) {
        chartMem.series[i].update({name: seriesname[i]}, false)
        chartMem.series[i].setData(series[i])
      }
    },
    getMax: function (legend) {
      var pos = this.legends_perc.indexOf(legend)
      var series = this.$store.state.dockerstats[0].data_perc[pos]
      var max = 0.00
      var min = 0.00
      var avg = 0.00
      var ret = []
      for (var i = 0; i < series.length; i++) {
        if (series[i][1] > max) {
          max = series[i][1]
          console.log(series[i][1])
        }
        if (series[i][1] > max) {
          max = series[i][1]
          console.log(series[i][1])
        }
        avg += series[i][1]
      }
      avg = avg / series.length
      max = max.toFixed(2)
      min = min.toFixed(2)
      avg = avg.toFixed(2)
      ret.push(max)
      ret.push(min)
      ret.push(avg)
      return ret
    },
    getMaxIO: function (legend) {
      var pos = this.legends_io.indexOf(legend)
      var series = this.$store.state.dockerstats[0].data_io[pos]
      var max = 0.00
      var min = 0.00
      var avg = 0.00
      var ret = []
      for (var i = 0; i < series.length; i++) {
        if (series[i][1] > max) {
          max = series[i][1]
        }
        if (series[i][1] > max) {
          max = series[i][1]
        }
        avg += series[i][1]
      }
      avg = avg / series.length
      ret.push(this.bytesToSize(max))
      ret.push(this.bytesToSize(min))
      ret.push(this.bytesToSize(avg))
      return ret
    },
    getMaxMeM: function (legend) {
      var pos = this.legends_mem.indexOf(legend)
      var series = this.$store.state.dockerstats[0].data_mem[pos]
      var max = 0.00
      var min = 0.00
      var avg = 0.00
      var ret = []
      for (var i = 0; i < series.length; i++) {
        if (series[i][1] > max) {
          max = series[i][1]
        }
        if (series[i][1] > max) {
          max = series[i][1]
        }
        avg += series[i][1]
      }
      avg = avg / series.length
      ret.push(this.bytesToSize(max))
      ret.push(this.bytesToSize(min))
      ret.push(this.bytesToSize(avg))
      return ret
    },
    bytesToSize: function (bytes) {
      var sizes = ['B', 'KB', 'MB', 'GB', 'TB']
      if (bytes === 0) {
        return '0 B'
      }
      var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)))
      return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i]
    },
    toggleSeriesChart: function (charttype, legend) {
      var chart
      var pos
      var series
      var elem = legend
      if (charttype === 'perc') {
        chart = this.$refs.highcharts.chart
        pos = this.legends_perc.indexOf(legend)
        series = this.$store.state.dockerstats[0].data_perc
      } else if (charttype === 'mem') {
        chart = this.$refs.highcharts_mem.chart
        pos = this.legends_mem.indexOf(legend)
        series = this.$store.state.dockerstats[0].data_mem
      } else {
        chart = this.$refs.highcharts_io.chart
        pos = this.legends_io.indexOf(legend)
        series = this.$store.state.dockerstats[0].data_io
      }
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
  }
}
</script>