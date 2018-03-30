<template>
    <div class="col-12 settings-container hub-parent-block">
       <div v-for="item in dappscategories" :key="item.category" class="dapps-category">
         {{item.name}}
         <div v-if="loadApps && item.category == dapp.category" v-for="(dapp,index) in dappsjson" :key="index" class="dapp-component">
           <img class="dapps-settings float-right" src="../../assets/images/settings-gray.svg"/>
           <img class="dapps-logo" :src="dapp.logo"/>
           <div>
             {{dapp.name}}
           </div>
         </div>
       </div>
    </div>
</template>

<script>
export default {
  name: 'dappsHubContent',
  props: ['loadApps'],
  computed: {
    dappscategories: {
      get: function () {
        return [{"name":"HELPER DAPPS","category":"helper"}, {"name":"IOP STACK","category":"iop-stack"}, {"name":"COMMUNITY DEV APPS","category":"community"}]
      }
    },
    dappsjson: {
      get: function () {
        debugger
        return this.$store.state.dappsjson
      }
    }
  }
}
</script>