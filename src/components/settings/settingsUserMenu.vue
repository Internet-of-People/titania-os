<template>
  <div class='col-12 settings-page'>
    <div class='col-12 settings-container'>
        <div class='settings-header'>USER LIST</div> 
        <div v-if="currentuser.length > 0" class='user-row'>
            <div class='sans-serif-bold'>{{currentuser}}</div>
        </div>
        <div v-for="user in users" v-if="currentuser !== user" :key="user" class='user-row'> 
            <div class='col-11'>{{user}}</div>
            <div class='col-1 float-right cursor-pointer' @click="deleteuser(user)" title='Delete user'>
                <img class="edit-remove-icon" src="../../assets/images/trash.svg"/>
            </div>
        </div>
        <div class='cursor-pointer float-left add-new display-inline-flex' @click="addNewUser()">
            <img class='margin-right-8' src="../../assets/images/icon-plus.svg">
            <div>Add new user</div>
        </div>
    </div>
    <div v-if="configure">
      <config-form :test-prop='tabname' ref="configFormDiv" />
      <div class="fadeout" @click="toggleConfig()"></div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import VueLocalStorage from 'vue-ls'
import configForm from '@/components/configuration/configForm'
Vue.use(VueLocalStorage)

export default {
  name: 'userlist',
  components: {
    configForm
  },
  computed: {
    users: {
      get: function () {
        return this.$store.state.settings.users
      }
    },
    currentuser: {
      get: function () {
        return Vue.ls.get('user')
      }
    },
    configure: {
      get: function () {
        return this.$store.state.settings.getform
      },
      set: function (value) {
        this.$store.state.settings.getform = value
      }
    },
    tabname: {
      get: function () {
        return 'user'
      }
    }
  },
  methods: {
    deleteuser: function (username) {
      console.log(username)
      var deleterequest = {}
      deleterequest.user = username
      this.$store.dispatch('deleteUser', deleterequest)
    },
    addNewUser: function () {
      this.configure = !this.configure
    },
    toggleConfig: function () {
      this.addNewUser()
    },
    submit: function (event) {
      if (event.which === 13) {
        // on enter press
        if ($('.center-aligned-slider').length === 0) {
          this.toggleConfig()
        } else {
          this.$refs.configFormDiv.saveConfig()
        }
      } else if (event.which === 27 && $('.center-aligned-slider').length === 1) {
        this.toggleConfig() // on esc press
      }
    }
  },
  created: function () {
    window.addEventListener('keyup', this.submit)
  },
  unmounted: function () {
    window.removeEventListener('keyup', this.submit)
  }
}
</script>
