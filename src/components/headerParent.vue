<template>
  <div class="header-inner-wrapper">
    <div class="page-title sans-serif-normal float-left regular-fontsize">{{getPageTitle(nameProp)}}</div>
    <div @click="logout()" class="toolbar-header-options cursor-pointer">
      LOGOUT
    </div>
    <div class='hide-mobile-menu' @click="openMenu()">
      <img src='../assets/images/menu-icon.svg'>
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
    },
    getPageTitle (pagename) {
      return pagename === 'DASHBOARD' ? 'DASHBOARD' : 'DASHBOARD  >  ' + pagename
    },
    openMenu () {
      this.$router.push('/menu')
    }
  }
}
</script>
