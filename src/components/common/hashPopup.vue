<template>
  <div class="float-left popup-window-hash outline-none">
    <div class="popup-content-hash">
      <div class="cursor-default">
        <div class="header-fontsize sans-serif-bold padding-top-bottom-16">HASH INFORMATION</div>
        <div class="padding-top-bottom-16">
            <div class="col-12">
                <div class="padding-left-16 sans-serif-normal text-align large-fontsize">Yocto Hash</div>
                <div @click="copyToClipboard('yocto')" class="hash-id-div" type="text">{{this.$store.state.build_id}}</div>
            </div>
            <div class="col-12">
                <div class="padding-left-16 sans-serif-normal text-align large-fontsize">UX Hash</div>
                <div @click="copyToClipboard('ux')" class="hash-id-div" type="text">{{this.$store.state.ux_id}}</div>
            </div>
        </div>
      </div>
      <div class="display-inline-flex popup-browser-primary-copy cursor-pointer outline-none regular-fontsize">
        <img src="../../assets/images/ic-copy.svg">
        <div @click="copyToClipboard('all')" class="padding-top-bottom-12">Copy Hash</div>
    </div>   
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
export default {
  name: 'hashPopup',
  computed: {
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
    copyToClipboard: function (txtformat) {
        var copytext = txtformat === "yocto"|| txtformat === "all"? "Yocto Hash: "+this.$store.state.build_id:""
        copytext += txtformat === "all"? ", ":"" 
        copytext += txtformat === "ux"||txtformat === "all"? "UX Hash: "+ this.$store.state.ux_id:""
        var aux = document.createElement("input")
        aux.setAttribute("value", copytext)
        document.body.appendChild(aux)
        aux.select()
        document.execCommand("copy")
        document.body.removeChild(aux)
        Vue.toast('Hash copied', {
              id: 'my-toast',
              className: ['toast-success'],
              horizontalPosition: 'right',
              verticalPosition: 'bottom',
              duration: 2000,
              mode: 'queue'
        })
    },
    submit: function () {
        // on esc press
        if (event.which === 27 && $('.popup-window-hash').length === 1) {
            this.hashPopupState = false
        }
    }
  },
  created: function () {
    window.addEventListener('keyup', this.submit)
  },
  unmounted: function () {
    window.removeEventListener('keyup', this.submit)
  }
}
</script>
