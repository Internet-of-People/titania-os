<template>
    <div id="container" class="position-absolute">
        <div class="titania-logo temp-logo-text">Titania</div>
        <div class='padding-top-bottom-16'>
            <input type="text" @keyup.enter="submit()" class="input_c small-fontsize outline-none" id="username" v-model="credentials.username" placeholder="Username"/>
        </div>
        <div class='padding-top-bottom-16'>
            <input type="text" @keyup.enter="submit()" class="input_c small-fontsize outline-none" placeholder="Password" v-model="credentials.password" id="password"/>
        </div>
        <button type="button" @click="submit()" @keyup.enter="submit()" class="outline-none small-fontsize button-primary" id="login_submit">LOGIN</button>
    </div>
</template>

<script>
export default {
  name: 'login',
  data () {
    return {
      credentials: {
        username: '',
        password: ''
      },
      error: ''
    }
  },
  methods: {
    submit () {
      const credentials = {
        username: this.credentials.username,
        password: this.credentials.password
      }
      // insert login auth code here
      console.log(credentials.username + ' ' + credentials.password)
    }
  }
}
</script>

<style scoped>
.titania-logo{
  width: 330px;
  height: 100px;
  margin: 40px auto 0 auto;
  //border: 1px solid #d8d8d8;
  vertical-align: middle;
}

.temp-logo-text{
  font-size: 74px;
}
</style>
