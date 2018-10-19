<template>
    <div class='threads-wrapper container-based-wrapper'>
        <div v-for="row in containerthreads" :key="row.container_name"  v-if="row.data.length > 0">
            <div class='float-left container-header'>{{row.container_name}} 
              <div class='display-inline-flex micro-fontsize'>({{row.container_id}})</div> 
            </div>
            <table class='col-12 threads-table container-threads-table'>
            <thead>
                <tr>
                <td>PID</td>
                <td>USER</td>
                <td>TIME</td>
                <td>COMMAND</td>
                </tr>
            </thead>
            <tbody>
                <tr v-for="r in row.data" :key="r[0]" v-if="r.length > 0"> 
                <td>{{r[0]}}</td>
                <td>{{r[1]}}</td>
                <td>{{r[2]}}</td>
                <td>{{r[3]}}</td>
                </tr>
            </tbody>
            </table>
    </div>
    <div class='hint-threads-container'>Data is shown only for running dApps</div>
  </div>
</template>


<script>
export default {
  name: 'threadsContainer',
  props: ['detailProp'],
  computed: {
    containerthreads: {
      get: function () {
        return this.$store.state.containerthreads
      }
    }
  },
  methods: {}
}
</script>
