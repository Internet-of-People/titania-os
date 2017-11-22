<template>
  <div class=''>
    <table class='col-12 threads-table'>
      <thead>
        <tr v-if="detailProp == 'HIDE DETAILS'">
          <th>PID</th>
          <th>PPID</th>
          <th>USER</th>
          <th>Stat</th>
          <th>VSZ</th>
          <th>%VSZ</th>
          <th>%CPU</th>
          <th>COMMAND</th>
        </tr>
        <tr v-else>
          <th>PID</th>
          <th>USER</th>
          <th>%CPU</th>
          <th>COMMAND</th>
        </tr>
      </thead>
      <tbody v-if="detailProp == 'HIDE DETAILS'">
        <tr v-for="row in threads" :key="row[0]"> 
          <td>{{row[0]}}</td>
          <td>{{row[1]}}</td>
          <td>{{row[2]}}</td>
          <td>{{row[3]}}</td>
          <td>{{row[4]}}</td>
          <td>{{row[5]}}</td>
          <td>{{row[6]}}</td>
          <td>{{row[7]}}</td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr v-for="row in threads" :key="row[0]"> 
          <td>{{row[0]}}</td>
          <td>{{row[3]}}</td>
          <td>{{row[6]}}</td>
          <td>{{row[7]}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

// ["PID", "PPID", "USER", "STAT", "VSZ", "%VSZ", "%CPU", "COMMAND"]

<script>
export default {
  name: 'threadsAll',
  props: ['detailProp'],
  computed: {
    threads: {
      get: function () {
        return this.$store.state.threads
      }
    }
  },
  methods: {}
}
</script>
