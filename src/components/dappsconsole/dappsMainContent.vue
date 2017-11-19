<template>
  <div class=''>
    <table class='col-12 dapps-table'>
      <thead>
        <tr>
          <td></td>
          <td>NAME</td>
          <td>RUNNING FOR</td>
          <td>LATEST ACTION</td>
          <td>COMMAND</td>
          <td>STATUS</td>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in dockerrows" :key="row.container_id"> 
          <td><span class="circle" v-bind:style="getClass(row.state)"></span></td>
          <td>{{row.name}}</td>
          <td>{{row.running_for}}</td>
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
        return 'background: #00882B;'
      } else if (statetype === 'Paused') {
        return 'background: #F0BB2B;'
      } else if (statetype === 'Exited') {
        return 'background: #C82506;'
      }
    }
  }
}
</script>
