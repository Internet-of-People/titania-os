<template>
    <div>
        <sidebarParent></sidebarParent>
        <headerParent :name-prop="page"></headerParent>
        <pageLoader v-if="false"></pageLoader>
        <dAppsHubContent/>
    </div>
</template>

<script>
import sidebarParent from '@/components/common/sidebarParent'
import headerParent from '@/components/common/headerParent'
import pageLoader from '@/components/common/pageLoader'
import dAppsHubContent from '@/components/dappshub/dAppsHubContent'

export default {
  name: 'dappshub',
  computed: {
    page () {
      return 'DAPPS HUB'
    }
  },
  components: {
    sidebarParent,
    headerParent,
    pageLoader,
    dAppsHubContent
  }
}
</script>
