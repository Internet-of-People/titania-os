<template>
    <div class="float-left hide center-aligned-slider outline-none">
      <div class="padding-20">
            <input id="boxname" name="boxname" v-model="configdetails.boxname" placeholder="Box name" class="sans-serif-bold box-name-field header-fontsize" type="text" maxLength="64" />
      </div>
      <div class ="configure-add-options-menu">
           <span id="config" @click="tabSwitch('Config')"  v-bind:class="{ activeTab: getActiveTab('Config')}" class="sans-serif-bold small-fontsize ">CONFIG</span>
           <span id="wireless" @click="tabSwitch('Wireless')" v-bind:class="{ activeTab: getActiveTab('Wireless')}" class="sans-serif-bold small-fontsize ">WIFI SETUP</span>
      </div>
      <div class="center-aligned-slider-body">
        <div v-if="currenttab == 'Config'">
          <div class="form-field-block col-12">
             <div class="sans-serif-normal micro-fontsize form-label">USERNAME</div>
             <input v-model="configdetails.username" class="form-input-field one-part-field col-11 outline-none sans-serif-normal regular-fontsize" type="text" />
          </div>
          <div class="form-field-block col-12">
             <div class="sans-serif-normal micro-fontsize form-label">PASSWORD</div>
             <input v-model="configdetails.password" class="form-input-field one-part-field outline-none sans-serif-normal regular-fontsize" type="password" />
          </div>
          <div class="form-field-block col-12">
             <div class="sans-serif-normal micro-fontsize form-label">CONFIRM PASSWORD</div>
             <input v-model="configdetails.confirmPassword" class="form-input-field one-part-field outline-none sans-serif-normal regular-fontsize" type="password" />
          </div>
        </div>
        <div v-else>
           wifi setup
        </div>
      </div>
      <div class="col-12">
        <button @click="saveConfig()" class="save-config float-left cursor-pointer outline-none small-fontsize">SAVE</button>
      </div>
  </div>
</template>

<script>
export default {
  props: [
    'closeConfigForm'
  ],
  name: 'configForm',
  data () {
    return {
      currenttab: 'Config',
      configdetails: {
        boxname: '',
        username: '',
        password: '',
        confirmPassword: ''
      }
    }
  },
  methods: {
    tabSwitch (tabname) {
      this.currenttab = tabname
    },
    getActiveTab (tabname) {
      return this.currenttab === tabname
    },
    saveConfig () {
      this.$store.commit('saveConfigForm', this.configdetails)
    }
  }
}
</script>
