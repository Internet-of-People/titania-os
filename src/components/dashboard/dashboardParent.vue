<template>
  <div>
    <sidebarParent></sidebarParent>
    <headerParent></headerParent>
    <div id="dashboard">
      <div>Titania dashboard</div>
    </div>
  </div>
</template>

<script>
import sidebarParent from '@/components/dashboard/sidebarParent'
import headerParent from '@/components/dashboard/headerParent'

export default {
  name: 'dashboard',
  components: {
    sidebarParent,
    headerParent
  }
}
</script>
