<template>
  <div v-bind:class="{ marginLeft40: !getFooterClass()}" class="footer-wrapper col-12">
    <div class='float-left cursor-default'>
      <span class='titania_version'>Titania {{this.$store.state.schema}}</span>
      <span class='copyright'>&copy;&nbsp; {{new Date().getFullYear()}} Libertaria</span>
      <span id='registeredto' class='registeredto hide' v-bind:class="{show : !getFooterClass()}">Registered to <span>{{username}}</span></span>
    </div>
    <div class='float-right footer-links padding-right-20'>
      <span class="padding-right-20"><a href="https://drive.google.com/file/d/11xDyBFACJYxrDQY4YNdiBqF8UFhgvpT9/view" target="_blank">White Paper</a></span>
      <span class="padding-right-20"><a id="titania_feedback" href="mailto:pooja.maheshwari247@gmail.com?subject=Feedback on Titania 1.0">Feedback</a></span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'footerParent',
  computed: {
    username: {
      get: function () {
        if (this.$store.state.currentPage === 'configure') {
          return true
        }
        return this.$store.state.credentials.username
      }
    }
  },
  methods: {
    getFooterClass () {
      var fullheader = this.$store.state.currentPage === 'login' || this.$store.state.currentPage === 'configure'
      return fullheader
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.footer-wrapper {
  position: fixed;
  bottom: 0px;
  left: 0px;
  color: #53585F;
  padding: 6px 16px;
  height: 18px;
  box-shadow: 0 0 10px 0 rgba(0,0,0,0.20);
  display: inline-block;
  z-index: 100;
  background-color: white;
}
.copyright {
  border-left: 1px solid #f2f2f2;
  padding-left: 5px;
  padding-right: 5px;
}
.registeredto {
  border-left: 1px solid #f2f2f2;
  padding-left: 5px;
}
.footer-links > span:hover {
  color: #0067C5;
}
</style>
