<template>
  <div>
    <div v-bind:class="{ marginLeft40: !getFooterClass()}" class="footer-wrapper col-12">
      <div class='float-left cursor-default desktop-footer-essentials'>
        <span class='titania_version'><a @click="getHashDetails()">{{this.$store.state.schema}}</a></span>
        <span class='copyright'>&copy;&nbsp; {{new Date().getFullYear()}} Libertaria</span>
        <span id='registeredto' class='registeredto hide' v-bind:class="{show : !getFooterClass()}">Logged in as: <span>{{username}}</span></span>
        <span id='registeredto' class='registeredto hide warn-text' v-bind:class="{show : !getFooterClass()}">
          <a v-if="this.$store.state.natpmp === '0'" href="https://portforward.com/router.htm" target="_blank">NATPMP: OFF</a></span>
      </div>
      <div class='float-right footer-links padding-right-20'>
        <span class="padding-right-20 white-paper-footer"><a href="https://drive.google.com/file/d/11xDyBFACJYxrDQY4YNdiBqF8UFhgvpT9/view" target="_blank">White Paper</a></span>
        <span v-if="this.$router.currentRoute.path !== '/'" class="padding-right-20 feedback-footer"><a id="titania_feedback" :href="getmailhref()">Feedback</a></span>
        <span v-else>
          <span v-if="updateState == 'initial'" class="padding-right-20 update-version-elem">
            <a id="update_version" @click="toggleUpdatePopup()">Update Version</a>
          </span>
          <span v-else-if="updateState == 'success'" class="reboot-screen padding-right-20 update-version-elem">
            <a id="update_version" @click="rebootSystem()">Reboot to apply</a>
          </span>
          <span id="myBar" v-else-if="updateState == 'failure'"  class="reboot-screen padding-right-20 update-version-elem">
            <a id="update_version" @click="setupUpdateAgain()">Try again</a>
          </span>
          <span id="myBar" v-else class="padding-right-20 update-version-elem">
            <a id="update_version">Updating {{getPercofUpdate()}}</a>
          </span>
        </span>
      </div>
      </div>
      <div>
    </div>
    <hashPopup v-if="hashPopupState"/>
    <div class="fadeout" v-if="hashPopupState" @click="getHashDetails()"></div>
    <updateWindow v-if="showupdatepopup" :update-status="updateState"/>
    <div class="fadeout" v-if="showupdatepopup" @click="toggleUpdatePopup()"></div>
  </div>
</template>

<script>
import Vue from 'vue'
import VueLocalStorage from 'vue-ls'
import updateWindow from '@/components/common/updateWindow'
import hashPopup from '@/components/common/hashPopup'

Vue.use(VueLocalStorage)

export default {
  name: 'footerParent',
  components: {
    hashPopup,
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
    hashPopupState: {
      get: function () {
        return this.$store.state.hashPopupState
      },
      set: function (newstate) {
        this.$store.state.hashPopupState = newstate
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
      var fullheader = this.$router.currentRoute.path !== '/'
      return fullheader
    },
    getmailhref () {
      var feedbackEmail = 'info@iop-ventures.com'
      return 'mailto:' + feedbackEmail + '?subject=Feedback on ' + this.$store.state.schema
    },
    getHashDetails () {
      this.hashPopupState = !this.hashPopupState
    },
    toggleUpdatePopup () {
      this.showupdatepopup = !this.showupdatepopup
    },
    rebootSystem () {
      this.$store.dispatch('rebootSystem')
    },
    getPercofUpdate () {
      var perc = this.$store.state.updateData.cur_percent ? this.$store.state.updateData.cur_percent : null
      var elem = document.getElementById("myBar")
      if (perc) {
          elem.style.width = perc + '%'
          return perc + '%'
      } else {
          return ''
      }
    },
    setupUpdateAgain () {
      this.updateState = 'initial'
      this.toggleUpdatePopup()
    }
  }
}
</script>
