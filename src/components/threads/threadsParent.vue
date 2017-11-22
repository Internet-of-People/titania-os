<template>
  <div>
    <sidebarParent></sidebarParent>
    <headerParent :name-prop="page"></headerParent>
    <div class='margin-20'>
        <div class='float-left display-inline-flex threads-filter'>
            <div @click="setFilter('all')" v-bind:class="{highlightedFilter: getSelectedFilter('all')}">SYSTEM THREADS</div>
            <div @click="setFilter('container')" v-bind:class="{highlightedFilter: getSelectedFilter('container')}">CONTAINER-LEVEL THREADS</div>
        </div>
        <div class='details' @click="getDetails()">{{details}}</div>
        <div class='threads-wrapper'>
            <threadsAll :detail-prop="details" v-if="getSelectedFilter('all')" ></threadsAll>
            <threadsContainer :detail-prop="details" v-else ></threadsContainer>
        </div>
    </div>
  </div>
</template>

<script>
import sidebarParent from '@/components/sidebarParent'
import headerParent from '@/components/headerParent'
import threadsAll from '@/components/threads/threadsAll'
import threadsContainer from '@/components/threads/threadsContainer'

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
    threadsContainer
  },
  mounted: function () {
    if (!this.$session.exists()) {
      this.$router.push('/login')
    } else {
      this.$store.dispatch('getThreads')
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
      if (this.details === 'HIDE DETAILS') {
        this.details = 'SHOW DETAILS'
      } else {
        this.details = 'HIDE DETAILS'
      }
    }
  }
}
</script>
