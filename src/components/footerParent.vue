<template>
  <div v-bind:class="{ marginLeft40: !getFooterClass()}" class="footer-wrapper col-12">
    <div class='float-left cursor-default desktop-footer-essentials'>
      <span class='titania_version'>{{this.$store.state.schema}}</span>
      <span class='copyright'>&copy;&nbsp; {{new Date().getFullYear()}} Libertaria</span>
      <span id='registeredto' class='registeredto hide' v-bind:class="{show : !getFooterClass()}">Logged in as: <span>{{username}}</span></span>
    </div>
    <div class='float-right footer-links padding-right-20'>
      <span class="padding-right-20 white-paper-footer"><a href="https://drive.google.com/file/d/11xDyBFACJYxrDQY4YNdiBqF8UFhgvpT9/view" target="_blank">White Paper</a></span>
      <span class="padding-right-20 feedback-footer"><a id="titania_feedback" :href="getmailhref()">Feedback</a></span>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import VueLocalStorage from 'vue-ls'

Vue.use(VueLocalStorage)

export default {
  name: 'footerParent',
  computed: {
    username: {
      get: function () {
        if (this.$store.state.currentPage === 'configure') {
          return true
        }
        return Vue.ls.get('user')
      }
    }
  },
  methods: {
    getFooterClass () {
      var fullheader = this.$store.state.currentPage === 'login' || this.$store.state.currentPage === 'configure'
      return fullheader
    },
    getmailhref () {
      var feedbackEmail = 'info@iop-ventures.com'
      return 'mailto:' + feedbackEmail + '?subject=Feedback on ' + this.$store.state.schema
    }
  }
}
</script>
