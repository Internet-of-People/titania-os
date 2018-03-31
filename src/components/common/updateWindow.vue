<template>
  <div class="float-left popup-window outline-none">
    <div v-if="updateStatus == 'initial'" class="popup-content">
      <div class="cursor-default">
        <div class="header-fontsize sans-serif-bold padding-top-bottom-16">UPDATE VERSION</div>
        <div class="popup-hint-text regular-fontsize">Download the update file from our <a class="link-text" target="_blank" href="https://discordapp.com/invite/gsRKp6T">Discord</a> channel</div>
      </div>
      <div class="display-block padding-top-bottom-16 margin-top-20">
        <div class="display-block cursor-default float-left margin-bottom-4 margin-left-16">Select file</div>
        <div class="display-inline-block popup-browser-drawer">
          <input id="updateInput" class="popup-input-drawer popup-input cursor-pointer outline-none regular-fontsize" value="text" type="file" aria-required="true">
        </div>
      </div>
    </div>
    <div v-else-if="updateStatus == 'success'" class="popup-content">
      <div class="cursor-default">
          <div class="header-fontsize-larger sans-serif-bold padding-top-16">UPDATE COMPLETE</div>
          <img class="padding-top-bottom-8" src="../../assets/images/img-message-success.svg">
          <div class="popup-hint-text regular-fontsize">Your update finished successfully.</div>
      </div>
    </div>
    <div v-else-if="updateStatus == 'failure'" class="popup-content">
      <div class="cursor-default">
          <div class="header-fontsize-larger sans-serif-bold padding-top-16">UPDATE ERROR</div>
          <img class="padding-top-bottom-8 err-update-img" src="../../assets/images/img-message-error.svg">
          <div class="popup-hint-text regular-fontsize">There was a problem with your update.</div>
          <div class="display-inline-flex padding-top-bottom-8">
            <input type="checkbox" class="popup-checkbox" checked>
            <div>Send error report</div>
          </div>
      </div>
    </div>
    <div class="popup-actions">
      <button @click="closePopup()" class="float-left popup-browser-secondary cursor-pointer outline-none regular-fontsize">Close</button>
      <button v-if="updateStatus == 'initial'" @click="updateOS()" class="popup-browser-primary float-right cursor-pointer outline-none regular-fontsize">Update</button>
      <button v-else-if="updateStatus == 'success'"  @click="rebootOS()" class="popup-browser-primary-big float-right cursor-pointer outline-none regular-fontsize">Reboot System</button>
      <button v-else-if="updateStatus == 'failure'" @click="retryupdate()" class="popup-browser-primary float-right cursor-pointer outline-none regular-fontsize">Retry</button>
    </div>    
  </div>
</template>
<script>

import Vue from 'vue'
export default {
  name: 'updateWindow',
  props: ['updateStatus', 'whenApplied'],
  computed: {
    showupdatepopup: {
      get: function () {
        return this.$store.state.showupdatepopup 
      },
      set: function (newstate) {
        this.$store.state.showupdatepopup = newstate
      }
    }
  },
  methods: {
    updateOS: function () {
      var updateDiv = document.getElementById('updateInput')
      if (updateDiv.files.length > 0) {
        this.$store.dispatch('updateOSImage')
        this.closePopup()
      } else {
        Vue.toast('Please select the update file', {
          id: 'my-toast',
          className: ['toast-warning'],
          horizontalPosition: 'right',
          verticalPosition: 'bottom',
          duration: 4000,
          mode: 'queue'
        })
      }    
    },
    retryupdate: function () {
      this.$store.dispatch('retryUpdate')
    },
    rebootOS: function () {
      this.$store.dispatch('rebootSystem')
      this.closePopup()
    },
    closePopup: function () {
      this.showupdatepopup = !this.showupdatepopup
    },
    keyup: function () {
      if (event.which === 27 && $('.popup-window').length === 1) {
        this.closePopup() // on esc press
      }
    }
  },
  created: function () {
    window.addEventListener('keyup', this.keyup)
  },
  unmounted: function () {
    window.removeEventListener('keyup', this.keyup)
  }
}
</script>
