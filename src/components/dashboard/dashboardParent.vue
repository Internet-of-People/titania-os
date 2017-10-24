<template>
  <div>
    <sidebarParent></sidebarParent>
    <headerParent></headerParent>
    <div class="margin-20">
      <dashboardMainContent></dashboardMainContent>
    </div>
  </div>
</template>

<script>
import sidebarParent from '@/components/dashboard/sidebarParent'
import headerParent from '@/components/dashboard/headerParent'
import dashboardMainContent from '@/components/dashboard/dashboardMainContent'

export default {
  name: 'dashboard',
  components: {
    sidebarParent,
    headerParent,
    dashboardMainContent
  }
}
</script>
