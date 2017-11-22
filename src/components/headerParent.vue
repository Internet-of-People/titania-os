<template>
  <div class="header-inner-wrapper">
    <div class="page-title sans-serif-normal float-left regular-fontsize">{{nameProp}}</div>
    <div @click="logout()" class="toolbar-header-options cursor-pointer">
      LOGOUT
    </div>
  </div>
</template>

<script>
export default {
  name: 'headerParent',
  props: ['nameProp'],
  methods: {
    logout () {
      this.$session.destroy()
      this.$router.push('/login')
      this.$store.state.currentPage = 'login'
    }
  }
}
</script>
