<template>
  <div>
    <div v-bind:class="{ marginLeft40: !getFooterClass()}" class="footer-wrapper col-12">
      <div class='float-left cursor-default desktop-footer-essentials'>
        <span class='titania_version'><a @click="getHashDetails()">{{this.$store.state.schema}}</a></span>
        <span class='copyright'>&copy;&nbsp; {{new Date().getFullYear()}} Libertaria</span>
        <span id='registeredto' class='registeredto hide' v-bind:class="{show : !getFooterClass()}">Logged in as: <span>{{username}}</span></span>
      </div>
      <div class='float-right footer-links padding-right-20'>
        <span class="padding-right-20 white-paper-footer"><a href="https://drive.google.com/file/d/11xDyBFACJYxrDQY4YNdiBqF8UFhgvpT9/view" target="_blank">White Paper</a></span>
        <span class="padding-right-20 feedback-footer"><a id="titania_feedback" :href="getmailhref()">Feedback</a></span>
      </div>
    </div>
    <hashPopup v-if="hashPopupState"/>
    <div class="fadeout" v-if="hashPopupState" @click="getHashDetails()"></div>
  </div>
</template>

<script>
import Vue from 'vue'
import VueLocalStorage from 'vue-ls'
import hashPopup from '@/components/common/hashPopup.vue'

Vue.use(VueLocalStorage)

export default {
  name: 'footerParent',
  components: {
    hashPopup
  },
  computed: {
    username: {
      get: function () {
        if (this.$store.state.currentPage === 'configure') {
          return true
        }
        return Vue.ls.get('user')
      }
    },
    hashPopupState: {
      get: function () {
        return this.$store.state.hashPopupState
      },
      set: function (newstate) {
        this.$store.state.hashPopupState = newstate
      }
    }
  },
  methods: {
    getFooterClass () {
      var fullheader = this.$store.state.currentPage === 'login' || this.$store.state.currentPage === 'configure' || this.$store.state.currentPage === 'landingpage'
      return fullheader
    },
    getmailhref () {
      var feedbackEmail = 'info@iop-ventures.com'
      return 'mailto:' + feedbackEmail + '?subject=Feedback on ' + this.$store.state.schema
    },
    getHashDetails () {
      this.hashPopupState = !this.hashPopupState
    }
  }
}
</script>
