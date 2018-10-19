<template>
  <div>
    <div class="col-12 store-container hub-parent-block">
      <div v-for="action in dappsstateactions" :key="action" class="float-left display-inline-flex threads-filter cursor-pointer" @click="changedAppFilter(action)">
        <div v-if="dappsFilter === action" class="highlightedFilter">
          {{action}}
        </div>
        <div v-else>{{action}}</div>
      </div>
      <div id="hub-loader" class="hide">
        <table>
            <tbody>
                <tr>
                    <td>
                        <div class="loader-mini">
                            <div class="loader-page">
                                <div></div>
                            </div>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
      </div>
      <div class="dapps-block">
        <div v-for="item in dappscategories" v-if="getIfContainsApp(dappsFilter, item.category)" :key="item.category" class="dapps-category">
          <div class="dapp-label display-inline-flex">{{item.name}}
              <div class="padding-left-16 link-text" v-if="item.category == 'community'"><a target="_blank" href="https://github.com/libertaria-project/titania-os/tree/develop/doc/dapp-guidelines.md">Dapp Guidelines</a></div>
          </div>
          <div class="dapp-block display-inline-flex">
            <div v-if="loadApps && item.category == dapp.tags && filterCheck(dapp.is_active)" 
                  v-for="(dapp,index) in dappsjson" :key="index" 
                  class="dapp-component cursor-pointer">
              <div :id="'update_'+ dapp.name.split(' ').join('_')" class="downloading-label" v-if="dapp.is_active !== -1 && dapp.is_active !== 2  && updatedapps.indexOf(dapp.id) !== -1" @click="optionAction('Update', dapp)">Update</div>
              <div class="downloading-label" v-if="dapp.is_active == 2">Downloading</div>
              <a v-if="item.category == 'community' && dapp.is_active == 1" :href="'/dapp/'+ dapp.id" target="_blank">
                <img class="dapps-logo" :src="dapp.logo" @click="getAppDetails(item.category,dapp)"/>
              </a>
              <a v-else>
                <img class="dapps-logo" :src="dapp.logo" @click="getAppDetails(item.category,dapp)"/>
              </a>
              <img class="dapps-settings" src="../../assets/images/ic-options.png" @click="openOptionsMenu(dapp)"/>
              <div class="dapp-name">
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
    </div>
    <dAppPopup v-if="showdappdetail" :dapp-details="activedapp" :dapp-states="dappstates" :active-category="activecategory"  :dapp-action="optionAction"/>
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
        return [{"name":"HELPER DAPPS","category":"helper"}, {"name":"IOP STACK","category":"core"}, {"name":"COMMUNITY DAPPS","category":"community"}]
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
    },
    updatedapps: {
      get: function () {
        return this.$store.state.updatedapps
      }
    },
    dappstates: {
      get: function () {
        return this.$store.state.dappstates
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
        if (dapp.is_active == this.dappstates.not_downloaded) {
          return ['Download', 'Details']
        } else if (dapp.is_active == this.dappstates.disabled) {
            if (category == 'community') {
              return ['Enable', 'Remove', 'Details']
            } else {
              return ['Enable', 'Details']
            }
        } else if (dapp.is_active == this.dappstates.enabled_and_active) {
          return ['Disable', 'Details']
        } else if (dapp.is_active == this.dappstates.enabled_and_not_active) {
          return ['Restart', 'Disable', 'Details']
        } else if (dapp.is_active == this.dappstates.downloading) {
          return ['Details']
        }
      }
    },
    optionAction: function(option, dapp) {
      this.showdappdetail = false
      $('.dropdown-config').addClass('hide')
      if (option === 'Details') {
        this.getAppDetails(option, dapp)
      } else if (option == 'Enable') {
        this.$store.dispatch('enableDapp', dapp.id) 
      } else if (option == 'Disable') {        
        this.$store.dispatch('disableDapp', dapp.id) 
      } else if (option == 'Restart') {
        this.$store.dispatch('restartDapp', dapp.id)
      } else if (option == 'Remove') {
        this.$store.dispatch('removeDapp', dapp) 
      } else if (option == 'Download') {
        // docker pull <container name>
        this.$store.dispatch('downloadDapp', dapp)
      } else if (option == 'Update') {
        $('#update_'+ dapp.name.split(' ').join('_')).text('Updating')
        this.$store.dispatch('updateDapp', dapp.id)
      }
    },
    getIfContainsApp: function(filter, category) {
      var enabled = 0, disabled = 0
      if (filter == 'AVAILABLE') {
        return true
      } else if (filter == 'INSTALLED') {
        for (var i = 0; i < this.dappsjson.length; i++) {
          if (this.dappsjson[i].is_active == 1 && this.dappsjson[i].tags[0]==category){
            enabled++
          } 
        }
        return enabled > 0
      } else {
        for (var i = 0; i < this.dappsjson.length; i++) {
          if (this.dappsjson[i].is_active == 0 && this.dappsjson[i].tags[0]==category){
              disabled++
          }
        }
        return disabled > 0
      }
    }
  }
}
</script>