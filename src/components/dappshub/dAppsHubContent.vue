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
            <img class="dapps-logo" :src="dapp.logo" @click="getAppDetails(item.category,dapp)"/>
            <img class="dapps-settings" src="../../assets/images/ic-options.png" @click="openOptionsMenu(dapp)"/>
            <div>
              {{dapp.name}}
            </div>
            <ul :id="dapp.name.replace(' ','_')" class='dropdown-config hide' >
                <li v-for="option in getdAppOptions(item.category, dapp)" :key="option" class="float-left  cursor-pointer col-11 selected" @click="optionAction(option, dapp)">
                  <span class="float-left cursor-pointer sans-serif-bold overflow-hidden" style="width: 100%;">{{option}}</span>
                </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <dAppPopup v-if="showdappdetail" :dapp-details="activedapp" :active-category="activecategory"/>
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
      get: function (action) {
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
    },
    activecategory: {
      get: function () {
        return this.$store.state.activecategory
      },
      set: function (value) {
        this.$store.state.activecategory = value
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
    getAppDetails: function (category, dapp) {
      $('.dropdown-config').addClass('hide')
      this.showdappdetail = !this.showdappdetail
      if (dapp) {
        this.activedapp = dapp
        this.activecategory = category
      } else {
        this.activedapp = {}
      }
    },
    openOptionsMenu: function (dapp) {
      var dropdownid = dapp.name.replace(' ','_')
      $('.dropdown-config').addClass('hide')
      $('#'+dropdownid).removeClass('hide')
    },
    getdAppOptions: function (category, dapp) {
      if (category == 'helper') {
        return ['Details']
      } else {
        if (dapp.is_active == -1) {
          return ['Download', 'Details']
        } else if (category == 'community') {
            if (dapp.is_active == '0') {
              return ['Enable', 'Remove', 'Details']
            } else {
              return ['Disable', 'Details']
            }
        } else{
            if (dapp.is_active == '0') {
              return ['Enable', 'Details']
            } else {
              return ['Disable', 'Details']
            }
        }
      }
    },
    optionAction: function(option, dapp) {
      $('.dropdown-config').addClass('hide')
      if (option === 'Details') {
        this.getAppDetails(option, dapp)
      } else if (option == 'Enable') {
        this.$store.dispatch('enableDapp', dapp.id) 
      } else if (option == 'Disable') {        
        this.$store.dispatch('disableDapp', dapp.id) 
      } else if (option == 'Remove') {
        this.$store.dispatch('removeDapp', dapp) 
      } else if (option == 'Download') {
        // docker pull <container name>
        this.$store.dispatch('downloadDapp', dapp)
      }
    }
  }
}
</script>