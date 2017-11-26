<template>
  <div class="clearfix single-events-div" @click="getDrilldown()">
    <div class="clearfix events-desc-div">
      <div class="overview-events float-left clearfix">
        <div class="overview-event-count total-servers">{{testProp[2]}}</div>
        <div class="overview-event-desc large-fontsize">{{testProp[1]}}</div>
        <div class="overview-event-icon"></div>
      </div>
      <div>
        <img v-if="testProp[1] === 'Total dApps'" class="overview-event-image" src="../../assets/images/dApps.png"></img>
        <img v-else-if="testProp[1] === 'Uptime'" class="overview-event-image" src="../../assets/images/uptime.png"></img>
        <img v-else-if="testProp[1] === 'Stopped dApps'" class="overview-event-image" src="../../assets/images/neigh_nodes.png"></img>
        <img v-else class="overview-event-image" src="../../assets/images/threads.png"></img>
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
        return 'Show container and system threads'
      } else {
        return 'Show container stats'
      }
    }
  }
}
</script>
