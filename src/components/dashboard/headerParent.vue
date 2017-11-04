<template>
  <div class="header-inner-wrapper">
    <div class="page-title sans-serif-normal float-left regular-fontsize" style="width: 109px;">DASHBOARD</div>
    <div @click="logout()" class="toolbar-header-options cursor-pointer">
      LOGOUT
    </div>
  </div>
</template>

<script>
export default {
  name: 'headerParent',
  methods: {
    logout () {
      this.$session.destroy()
      this.$router.push('/login')
    }
  }
}
</script>
