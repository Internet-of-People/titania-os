<template>
  <div class='col-12'>
    <div class='col-12 settings-container'>
        <div class='settings-header'>USER LIST</div> 
        <div v-if="currentuser.length > 0" class='user-row'>
            <div class='sans-serif-bold'>{{currentuser}}</div>
        </div>
        <div v-for="user in users" v-if="currentuser !== user" :key="user" class='user-row'> 
            <div class='col-11'>{{user}}</div>
            <div class='col-1 float-right cursor-pointer' @click="deleteuser(user)">
                <img class="" src="../../assets/images/icon-plus.svg"/>
            </div>
        </div>
        <div class='float-left add-new display-inline-flex'>
            <img class='margin-right-8' src="../../assets/images/icon-plus.svg">
            <div>Add new user</div>
        </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import VueLocalStorage from 'vue-ls'

Vue.use(VueLocalStorage)

export default {
  name: 'userlist',
  components: {
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
    }
  },
  methods: {
    deleteuser: function (username) {
      console.log(username)
      var deleterequest = {}
      deleterequest.user = username
      this.$store.dispatch('deleteUser', deleterequest)
    }
  }
}
</script>
