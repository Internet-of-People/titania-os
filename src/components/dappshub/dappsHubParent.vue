<template>
    <div>
        <sidebarParent></sidebarParent>
        <headerParent :name-prop="page"></headerParent>
        <pageLoader v-if="false"></pageLoader>
        <dappsHubContent/>
    </div>
</template>

<script>
import sidebarParent from '@/components/common/sidebarParent'
import headerParent from '@/components/common/headerParent'
import pageLoader from '@/components/common/pageLoader'
import dappsHubContent from '@/components/dappshub/dappsHubContent'

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
    dappsHubContent
  }
}
</script>
