<template>
    <div class="float-left popup-window outline-none">
        <div class="dapp-popup-header-block">
           <img class="dapp-popup-logo" :src="dappDetails.logo"/>
           <div class="dapp-popup-name">{{dappDetails.name}}</div>
           <div v-if="activeCategory!='helper'" class="dapps-popup-action-items">
               <button v-if="dappDetails.is_active == '-1'" class="popup-browser-primary float-right cursor-pointer outline-none regular-fontsize">Download</button>
               <button v-if="dappDetails.is_active == '0'" class="popup-browser-primary float-right cursor-pointer outline-none regular-fontsize">Enable</button>
               <button v-if="dappDetails.is_active == '1'" class="popup-browser-primary float-right cursor-pointer outline-none regular-fontsize">Disable</button>
               <button v-if="dappDetails.is_active == '0'" class="popup-browser-primary float-right cursor-pointer outline-none regular-fontsize">Remove</button>
           </div>
        </div>
        <div class="dapps-popup-desc">
            <div class="float-left sans-serif-bold display-block">DESCRIPTION</div>
            <div>{{dappDetails.description}}</div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'dAppPopup',
  props: ['dappDetails','activeCategory']
}
</script>


