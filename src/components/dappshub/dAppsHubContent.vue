<template>
    <div class="col-12 settings-container hub-parent-block">
       <div v-for="item in dappscategories" :key="item" class="dapps-category">
         {{item}}
         <div class="dapp-component">
           <img class="dapps-settings float-right" src="../../assets/images/settings-gray.svg"/>
           <img class="dapps-logo" :src="dappsjson[0].logo"/>
           <div>
             {{dappsjson[0].name}}
           </div>
         </div>
       </div>
    </div>
</template>

<script>
export default {
  name: 'dappsHubContent',
  computed: {
    dappscategories: {
      get: function () {
        return ['HELPER DAPPS', 'IOP STACK', 'COMMUNITY DEV APPS']
      }
    },
    dappsjson: {
      get: function () {
        return this.$store.state.dappsjson
      }
    }
  }
}
</script>