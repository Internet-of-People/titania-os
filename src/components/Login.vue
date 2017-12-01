<template>
    <div id="container" >
        <img class="logo-icon" src="../assets/images/titania-Logo-port.svg">
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
    if (this.$session.exists()) {
      this.$router.push('/')
    }
  },
  beforeDestory: function () {
    this.$session.start()
  },
  methods: {
    submit () {
      this.$store.dispatch('login', this.$store.state.credentials)
    }
  }
}
</script>
