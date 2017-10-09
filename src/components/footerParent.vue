<template>
  <div class='footer-wrapper'>
    <div class='float-left'>
      <span class='titania_version'>Titania 1.0</span>
      <span class='copyright'>&copy;&nbsp; {{new Date().getFullYear()}} Libertaria</span>
      <span id='registeredto' class='registeredto'>Registered to user</span>
    </div>
    <div class='float-right footer-links padding-right-20'>
      <span class="padding-right-20"><a href="titania-link-to-documentation" target="_blank">Documentation</a></span>
      <span class="padding-right-20"><a id="titania_feedback" href="mailto:support@titania_libertaria.com">Feedback</a></span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'footerParent',
  data () {
    return {
      msg: 'Welcome aboard, Titania'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
div, a{
  font-size: 13px;
  font-family: "Segoe UI", "SF UI text", sans-serif !important;
}
.footer-wrapper {
  position: absolute;
  bottom: 0px;
  left: 0px;
  color: #53585F;
  padding: 6px 16px;
  height: 18px;
  border-top: 2px solid #F0F0F0;
  display: inline-block;
  width: 100%;
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
.float-left{
  float: left;
}
.float-right{
  float: right;
}
a{
  cursor: pointer;
  text-decoration: none;
  color: inherit;
  outline: none;
}
.padding-right-20{
  padding-right: 20px;
}
</style>
