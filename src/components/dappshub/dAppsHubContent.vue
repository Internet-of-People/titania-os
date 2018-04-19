<template>
  <div>
    <div class="col-12 settings-container hub-parent-block">
      <div v-for="action in dappsstateactions" :key="action" class="float-left display-inline-flex threads-filter cursor-pointer" @click="changedAppFilter(action)">
        <div v-if="dappsFilter === action" class="highlightedFilter">
          {{action}}
        </div>
        <div v-else>{{action}}</div>
      </div>
      <div class="dapps-block">
        <div v-for="item in dappscategories" :key="item.category" class="dapps-category">
          <div>{{item.name}}</div>
          <div v-if="loadApps && item.category == dapp.tags && filterCheck(dapp.is_active)" 
                v-for="(dapp,index) in dappsjson" :key="index" 
                class="dapp-component cursor-pointer">
            <img class="dapps-logo" :src="dapp.logo" @click="getAppDetails(dapp)"/>
            <img class="dapps-settings" src="../../assets/images/ic-options.png" @click="openOptionsMenu(dapp)"/>
            <div>
              {{dapp.name}}
            </div>
            <ul :id="dapp.name.replace(' ','_')" class='dropdown-config hide' >
                <li v-for="item in dappsoptions" :key="item" class="float-left  cursor-pointer col-11 selected" >
                  <span class="float-left cursor-pointer sans-serif-bold overflow-hidden" style="width: 100%;">{{item}}</span>
                </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <dAppPopup v-if="showdappdetail" :dapp-details="activedapp"/>
    <div class="fadeout" v-if="showdappdetail" @click="getAppDetails()"></div>
  </div>
</template>

<script>
import dAppPopup from '@/components/dappshub/dAppPopup.vue'
export default {
  name: 'dappsHubContent',
  components: {
    dAppPopup
  },
  props: ['loadApps'],
  computed: {
    dappsstateactions: {
      get: function () {
        return ["AVAILABLE", "INSTALLED", "DISABLED"]
      }
    },
    dappsoptions: {
      get: function () {
        return ["Install", "Disable", "Remove"]
      }
    },
    dappsFilter: {
      get: function () {
        return this.$store.state.dappsFilter
      },
      set: function (value) {
        this.$store.state.dappsFilter = value
      }
    },
    dappscategories: {
      get: function () {
        return [{"name":"HELPER DAPPS","category":"helper"}, {"name":"IOP STACK","category":"core"}, {"name":"COMMUNITY DEV APPS","category":"community"}]
      }
    },
    dappsjson: {
      get: function () {
        return this.$store.state.dappsjson
      }
    },
    showdappdetail: {
      get: function () {
        return this.$store.state.showdappdetail
      },
      set: function (value) {
        this.$store.state.showdappdetail = value
      }
    },
    activedapp: {
      get: function () {
        return this.$store.state.activedapp
      },
      set: function (value) {
        this.$store.state.activedapp = value
      }
    }
  },
  methods: {
    changedAppFilter: function (newfilter) {
      this.dappsFilter = newfilter
    },
    filterCheck: function (isactive) {
      var ret = true;
      if (this.dappsFilter == 'DISABLED') {
        ret = isactive == '0'
      } else if (this.dappsFilter == 'INSTALLED') {
        ret = isactive != '0'
      }
      return ret
    },
    getAppDetails: function (dapp) {
      this.showdappdetail = !this.showdappdetail
      if (dapp) {
        this.activedapp = dapp
      } else {
        this.activedapp = {}
      }
    },
    openOptionsMenu: function (dapp) {
      var dropdownid = dapp.name.replace(' ','_')
      $('#'+dropdownid).removeClass('hide')
    }
  }
}
</script>