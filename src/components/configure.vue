<template>
  <div>
    <div>
      <img src="../assets/images/titania-logo.png">
      <h1>{{ msg }}</h1>
    </div>
    <button type="button" @click="submit()" @keyup.enter="submit()" class="outline-none small-fontsize button-primary" id="login_submit">CONFIGURE</button>
  </div>
</template>

<script>
export default {
  name: 'configure',
  data () {
    return {
      msg: 'Welcome aboard, Titania'
    }
  },
  methods: {
    submit () {
      console.log(this.msg)
    }
  }
}
</script>
