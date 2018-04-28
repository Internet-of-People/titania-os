<template>
  <div>
    <sidebarParent></sidebarParent>
    <headerParent :name-prop="page"></headerParent>
    <div class='margin-20' v-if="this.$store.state.threads.length !== 0">
        <div class='float-left display-inline-flex threads-filter'>
            <div @click="setFilter('all')" v-bind:class="{highlightedFilter: getSelectedFilter('all')}">SYSTEM THREADS</div>
            <div @click="setFilter('container')" v-bind:class="{highlightedFilter: getSelectedFilter('container')}">CONTAINER-LEVEL THREADS</div>
        </div>
        <div class='details' v-if="getSelectedFilter('all')" @click="getDetails()">{{details}}</div>
        <div>
            <threadsAll :detail-prop="details" v-if="getSelectedFilter('all')" ></threadsAll>
            <threadsContainer :detail-prop="details" v-else ></threadsContainer>
        </div>
    </div>
    <pageLoader v-if="this.$store.state.threads.length === 0"></pageLoader>
  </div>
</template>

<script>
import sidebarParent from '@/components/common/sidebarParent'
import headerParent from '@/components/common/headerParent'
import threadsAll from '@/components/threads/threadsAll'
import threadsContainer from '@/components/threads/threadsContainer'
import pageLoader from '@/components/common/pageLoader'

export default {
  name: 'threads',
  computed: {
    page () {
      return 'THREADS'
    },
    threadfilter: {
      get: function () {
        return this.$store.state.threadfilter
      },
      set: function (newfilter) {
        this.$store.state.threadfilter = newfilter
      }
    },
    details: {
      get: function () {
        return this.$store.state.showDetails
      },
      set: function (newdetails) {
        this.$store.state.showDetails = newdetails
      }
    }
  },
  components: {
    sidebarParent,
    headerParent,
    threadsAll,
    threadsContainer,
    pageLoader
  },
  mounted: function () {
    if (!this.$session.exists()) {
      this.$router.push('/login')
      this.$store.state.currentPage = 'login'
    } else {
      this.$store.dispatch('getThreads')
      this.$store.state.currentPage = 'threads'
    }
  },
  methods: {
    getSelectedFilter (filter) {
      return filter === this.threadfilter
    },
    setFilter (filter) {
      this.threadfilter = filter
      if (filter === 'all') {
        this.$store.dispatch('getThreads')
      } else {
        this.$store.dispatch('getContainerTop')
      }
    },
    getDetails () {
      if (this.details === 'Hide details') {
        this.details = 'Show details'
      } else {
        this.details = 'Hide details'
      }
    }
  }
}
</script>
