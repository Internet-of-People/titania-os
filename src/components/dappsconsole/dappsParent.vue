<template>
  <div>
    <sidebarParent></sidebarParent>
    <headerParent :name-prop="page"></headerParent>
    <div class="margin-20 text-align">
      <div class='col-12'>
      <div class="display-inline-flex">
        <div class='float-right display-inline-flex'>
          <div class="label-wrapper">STATUS</div>
          <div class="float-right state-picker">Running <span class='float-right'>&#9662;</span></div>
        </div>
        <div class="label-wrapper">REFRESH EVERY</div>
        <div class='display-inline-flex padding-left-4'>
        <input type="number" class="col-2 outline-none sans-serif-normal small-fontsize" value="1">
        <div class="label-text outline-none sans-serif-normal regular-fontsize">Second(s)</div>
        
      </div>
      <div>HIDE DETAILS</div>
      </div>
      </div>
      <div class='general-wrapper-table'>
        <dappsMainContent></dappsMainContent>
      </div>
    </div>
  </div>
</template>

<script>
import sidebarParent from '@/components/sidebarParent'
import headerParent from '@/components/headerParent'
import dappsMainContent from '@/components/dappsconsole/dappsMainContent'

export default {
  name: 'dashboard',
  computed: {
    page () {
      return 'DAPPS CONSOLE'
    }
  },
  components: {
    sidebarParent,
    headerParent,
    dappsMainContent
  },
  mounted: function () {
    if (this.$route.params.setSession) {
      this.$session.start()
      this.$store.dispatch('getDockerOverview')
    } else if (!this.$session.exists()) {
      this.$router.push('/login')
    } else {
      this.$store.dispatch('getDockerOverview')
    }
  }
}
</script>
