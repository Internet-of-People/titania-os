<template>
  <div class="clearfix single-events-div" @click="getDrilldown()">
    <div class="clearfix events-desc-div">
      <div class="overview-events float-left clearfix">
        <div v-if="testProp[1] === 'Uptime'" class="overview-event-count total-servers" >{{secondsToHms(testProp[2])}}</div>
        <div v-else-if="testProp[1] === 'Threads'" class="overview-event-count total-servers" >{{nFormatter(testProp[2])}}</div>
        <div v-else class="overview-event-count total-servers">{{testProp[2]}}</div>
        <div class="overview-event-desc large-fontsize">{{testProp[1]}}</div>
        <div class="overview-event-icon"></div>
      </div>
      <div>
        <img v-if="testProp[1] === 'Total dApps'" class="overview-event-image" src="../../assets/images/boxes-icon.svg"/>
        <img v-else-if="testProp[1] === 'Uptime'" class="overview-event-image" src="../../assets/images/uptime-icon.svg"/>
        <img v-else-if="testProp[1] === 'Stopped dApps'" class="overview-event-image" src="../../assets/images/stopped-dapps-icon.svg"/>
        <img v-else class="overview-event-image" src="../../assets/images/thread-icon.svg"/>
      </div>
    </div>
    <div class="overview-events-link-div">
      <span class="overview-events-link-desc regular-fontsize" id="owlinkdesc">{{getHelpText()}}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'dashboardCard',
  props: ['testProp'],
  methods: {
    getDrilldown () {
      var cardtype = this.testProp[1]
      if (cardtype === 'Total dApps') {
        this.$router.push('/dappsconsole')
      } else if (cardtype === 'Stopped dApps') {
        this.$router.push({name: 'dappsconsole', params: { stopped: true }})
      } else if (cardtype === 'Threads') {
        this.$router.push('/threads')
      } else {
        this.$router.push('/stats')
      }
      // router.push({name: 'dashboard', params: { setSession: true }})
    },
    getHelpText () {
      var cardtype = this.testProp[1]
      if (cardtype === 'Total dApps') {
        return 'Show all dApps'
      } else if (cardtype === 'Stopped dApps') {
        return 'Show exited dApps'
      } else if (cardtype === 'Threads') {
        return 'Show running threads'
      } else {
        return 'Show container stats'
      }
    },
    secondsToHms (d) {
      d = Number(d)
      var day = Math.floor(d / (3600*24))
      var h = Math.floor(d / 3600)
      var m = Math.floor(d % 3600 / 60)
      var s = Math.floor(d % 3600 % 60)

      var dDisplay = day > 0 ? day + ':' + (h.toString().length >1 ? day : '0' + h) + ' day ' : ''
      var hDisplay = h > 0 && d == 0 ? h + ':' + (m.toString().length > 1 ? m : '0' + m) + ' h ' : ''
      var mDisplay = m > 0 && h === 0 ? m + ':' + (s.toString().length > 1 ? s : '0' + s) + ' m ' : ''
      var sDisplay = s > 0 && m === 0 ? s + ' s' : ''
      return dDisplay + hDisplay + mDisplay + sDisplay
    },
    nFormatter (num) {
      if (num >= 1000000000) {
        return (num / 1000000000).toFixed(1).replace(/\.0$/, '') + 'G'
      }
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
      }
      if (num >= 1000) {
        return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
      }
      return num
    }
  }
}
</script>
