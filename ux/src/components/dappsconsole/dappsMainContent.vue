<template>
  <div class=''>
    <table class='col-12 dapps-table'>
      <thead>
        <tr v-if="detailProp == 'Hide details'">
          <td></td>
          <td>NAME</td>
          <td>CONTAINER ID</td>
          <!-- <td>RUNNING FOR</td> -->
          <td>LATEST ACTION</td>
          <td>COMMAND</td>
          <td>STATUS</td>
          <td>NETWORKS</td>
        </tr>
        <tr v-else>
          <td></td>
          <td>NAME</td>
          <!-- <td>RUNNING FOR</td> -->
          <td>LATEST ACTION</td>
          <td>COMMAND</td>
          <td>STATUS</td>
        </tr>
      </thead>
      <tbody v-if="detailProp == 'Hide details'">
        <tr v-for="row in dockerrows" :key="row.container_id" v-if="showRow(row.state)"> 
          <td>
            <img class='state-dapps' v-if="row.state === 'Running'" src="../../assets/images/state-running.svg"/>
            <img class='state-dapps' v-else-if="row.state === 'Paused'" src="../../assets/images/state-paused.svg"/>
            <img class='state-dapps' v-else src="../../assets/images/state-stopped.svg"/>
          </td>
          <td>{{row.name}}</td>
          <td>{{row.container_id}}</td>
          <!-- <td>{{row.running_for}}</td> -->
          <td>{{row.status}}</td>
          <td>{{row.command}}</td>
          <td>{{row.state}}</td>
          <td>{{row.networks}}</td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr v-for="row in dockerrows" :key="row.container_id" v-if="showRow(row.state)"> 
          <td>
            <img class='state-dapps' v-if="row.state === 'Running'" src="../../assets/images/state-running.svg"/>
            <img class='state-dapps' v-else-if="row.state === 'Paused'" src="../../assets/images/state-paused.svg"/>
            <img class='state-dapps' v-else src="../../assets/images/state-stopped.svg"/>
          </td>
          <td>{{row.name}}</td>
          <!-- <td>{{row.running_for}}</td> -->
          <td>{{row.status}}</td>
          <td>{{row.command}}</td>
          <td>{{row.state}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

// [{"container_id": "1cd7228e69a4", "name": "competent_bell", "image": "hello-world", 
// "running_for": "19 minutes", "command": "\"/hello\"", "ports": "", 
// "status": "Exited (0) 19 minutes ago", "networks": "bridge"}, 
// {"container_id": "9c182da86d1e", "name": "nginx", "image": "libertaria/nginx:armv7",
//  "running_for": "15 hours", "command": "\"nginx -g 'daemon ...\"", 
//  "ports": "0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp", "status": "Up About an hour", "networks": "bridge"}]

<script>
export default {
  name: 'dappsMainContent',
  props: ['detailProp', 'stateProp'],
  computed: {
    dockerrows: {
      get: function () {
        return this.$store.state.dockeroverview
      }
    }
  },
  methods: {
    getClass (statetype) {
      if (statetype === 'Running') {
        return '../../assets/images/state-running.svg'
      } else if (statetype === 'Paused') {
        return 'background: #F0BB2B;'
      } else if (statetype === 'Exited') {
        return 'background: #C82506;'
      }
    },
    showRow (rowstate) {
      if (this.stateProp === 'All') {
        return true
      } else if (this.stateProp === rowstate) {
        return true
      }
      return false
    }
  }
}
</script>
