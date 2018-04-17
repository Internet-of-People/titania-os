<template>
    <div id="container" >
        <img class="logo-icon" src="../../assets/images/titania-Logo-port.svg">
        <div class='padding-top-bottom-16'>
            <input type="text" @keyup.enter="submit()" class="input_c regular-fontsize outline-none" id="username" v-model="username" placeholder="TitaniaUser"/>
        </div>
        <div class='padding-top-bottom-16'>
            <input type="password" @keyup.enter="submit()" class="input_c regular-fontsize outline-none" placeholder="Password" v-model="password" id="password"/>
        </div>
        <button type="button" @click="submit()" @keyup.enter="submit()" class="outline-none large-fontsize button-primary" id="login_submit">LOGIN</button>
    </div>
</template>

<script>
import Vue from 'vue'
export default {
  name: 'login',
  computed: {
    username: {
      get: function () {
        return this.$store.state.credentials.username
      },
      set: function (newUsername) {
        this.$store.state.credentials.username = newUsername
      }
    },
    password: {
      get: function () {
        return this.$store.state.credentials.password
      },
      set: function (newPassword) {
        this.$store.state.credentials.password = newPassword
      }
    }
  },
  beforeCreate: function () {
    if (this.$route.params && this.$route.params.deletesession) {
      this.$session.destroy()
    }
    if (this.$session.exists()) {
      this.$router.push('/')
    }
  },
  beforeDestory: function () {
    this.$session.destory()
    this.$session.start()
  },
  methods: {
    submit () {
      if (this.username.length === 0) {
        Vue.toast('Enter Username', {
          id: 'my-toast',
          className: ['toast-warning'],
          horizontalPosition: 'right',
          verticalPosition: 'bottom',
          duration: 4000,
          mode: 'queue',
          transition: 'my-transition'
        })
        $('#username').addClass('error-hint')
        return
      }
      $('#username').removeClass('error-hint')
      $('body').css('cursor', 'progress')
      $('#login_submit').css('cursor', 'wait')
      this.$store.dispatch('login', this.$store.state.credentials)
    }
  },
  mounted () {
    // this.$store.dispatch('initApp')
  }
}
</script>
