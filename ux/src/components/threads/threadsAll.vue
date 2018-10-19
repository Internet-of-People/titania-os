<template>
  <div class='threads-wrapper'>
    <table class='col-12 threads-table'>
      <thead>
        <tr v-if="detailProp == 'Hide details'">
          <th></th>
          <th class="col-3">PID</th>
          <th class="col-3">PPID</th>
          <th class="col-3">USER</th>
          <th class="col-3">Stat</th>
          <th class="col-3">VSZ</th>
          <th class="col-3">%VSZ</th>
          <th class="col-3">%CPU</th>
          <th class="col-5">COMMAND</th>
        </tr>
        <tr v-else>
          <th></th>
          <th class="col-3">PID</th>
          <th class="col-3">USER</th>
          <th class="col-3">%CPU</th>
          <th class="col-7">COMMAND</th>
        </tr>
      </thead>
      <tbody v-if="detailProp == 'Hide details'">
        <tr v-for="row in threads" :key="row[0]"> 
          <td></td>
          <td>{{row[0]}}</td>
          <td>{{row[1]}}</td>
          <td>{{row[2]}}</td>
          <td>{{row[3]}}</td>
          <td>{{row[4]}}</td>
          <td>{{row[5]}}</td>
          <td>{{row[6]}}</td>
          <td class="display-block">
            <div class="display-inline-flex">
              <div v-bind:key="i" v-for="i in row.length" class="margin-right-4">
                {{row[i+6]}}
              </div>
            </div>
          </td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr v-for="row in threads" :key="row[0]"> 
          <td></td>
          <td>{{row[0]}}</td>
          <td>{{row[3]}}</td>
          <td>{{row[6]}}</td>
          <td class="display-block">
            <div class="display-inline-flex">
              <div v-bind:key="i" v-for="i in row.length" class="margin-right-4">
                {{row[i+6]}}
              </div>
            </div>
          </td>
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
