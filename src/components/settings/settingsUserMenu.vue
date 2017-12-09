<template>
  <div class='col-12'>
    <div class='col-12 settings-container'>
        <div class='settings-header'>USER LIST</div> 
        <div v-for="user in users" :key="user" class='user-row'> 
            <div class='col-10'>{{user}}</div>
            <div class='col-1 float-right'>
                <img class="" src="../../assets/images/icon-plus.svg"/>
            </div>
            <div class='col-1 float-right'>
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

export default {
  name: 'userlist',
  components: {
  },
  computed: {
    users: {
      get: function () {
        return this.$store.state.settings.users
      }
    }
  }
}
</script>
