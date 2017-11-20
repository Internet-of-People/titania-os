<template>
    <div>
          <div class='container-holder'>{{testProp.container_name}}</div>
          <highcharts class='chart-other' :options="options" ref="highcharts"></highcharts>
    </div>
</template>

<script>

export default {
  name: 'containerChart',
  props: ['testProp'],
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
    //   var chart
    //   var nameType
      var chart = this.$refs.highcharts
      // var series = this.testProp
      console.log(chart)
    //   chart.series[/].setData(series[i].data[0][name])
    //   chart.series[j].update({name: nameType}, false)
    //     for (var j = 0; j < series[i].data.length; j++) {
    //       nameType = Object.keys(series[i].data[j])[0]
    //       chart.series[j].setData(series[i].data[0][name])
    //       chart.series[j].update({name: nameType}, false)
    //     }
    //   }
    }
  },
  mounted: function () {
    this.updateCredits()
  }
}
</script>