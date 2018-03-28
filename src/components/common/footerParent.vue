<template>
  <div>
    <div v-bind:class="{ marginLeft40: !getFooterClass()}" class="footer-wrapper col-12">
      <div class='float-left cursor-default desktop-footer-essentials'>
        <span class='titania_version'>{{this.$store.state.schema}}</span>
        <span class='copyright'>&copy;&nbsp; {{new Date().getFullYear()}} Libertaria</span>
        <span id='registeredto' class='registeredto hide' v-bind:class="{show : !getFooterClass()}">Logged in as: <span>{{username}}</span></span>
      </div>
      <div class='float-right footer-links padding-right-20'>
        <span class="padding-right-20 white-paper-footer"><a href="https://drive.google.com/file/d/11xDyBFACJYxrDQY4YNdiBqF8UFhgvpT9/view" target="_blank">White Paper</a></span>
        <span class="padding-right-20 feedback-footer"><a id="titania_feedback" :href="getmailhref()">Feedback</a></span>
        <span v-if="!getFooterClass()">
          <span v-if="updateState == 'initial'" class="padding-right-20 update-version-elem"><a id="update_version" @click="toggleUpdatePopup()">Update Version</a></span>
          <span v-else-if="updateState == 'success'" class="padding-right-20 update-version-elem"><a id="update_version" @click="rebootSystem()">Reboot to apply</a></span>
          <span v-else class="padding-right-20 update-version-elem"><a id="update_version">Updating</a></span>
        </span>
      </div>
    </div>
    <updateWindow v-if="showupdatepopup" :update-status="updateState"/>
    <div class="fadeout" v-if="showupdatepopup" @click="toggleUpdatePopup()"></div>
  </div>
</template>

<script>
import Vue from 'vue'
import VueLocalStorage from 'vue-ls'
import updateWindow from '@/components/common/updateWindow'

Vue.use(VueLocalStorage)

export default {
  name: 'footerParent',
  components: {
    updateWindow
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
    showupdatepopup: {
      get: function () {
        return this.$store.state.showupdatepopup 
      },
      set: function (newstate) {
        this.$store.state.showupdatepopup = newstate
      }
    },
    updateState: {
      get: function () {
        return this.$store.state.updateState 
      },
      set: function (newstate) {
        this.$store.state.updateState = newstate
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
    toggleUpdatePopup () {
      this.showupdatepopup = !this.showupdatepopup
    },
    rebootSystem () {
      this.$store.dispatch('rebootSystem')
    }
  }
}
</script>
