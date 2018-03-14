<template>
  <div class="float-left popup-window outline-none">
    <div class="popup-content">
      <div class="cursor-default">
        <div class="header-fontsize padding-top-bottom-16">UPDATE VERSION</div>
        <div class="popup-hint-text regular-fontsize">Download the update file from our <a class="link-text" href="https://discordapp.com/invite/gsRKp6T">Discord</a> channel</div>
      </div>
      <div class="display-block padding-top-bottom-16 margin-top-20">
        <div class="display-block cursor-default float-left margin-bottom-4 margin-left-16">Select file</div>
        <div class="display-inline-block popup-browser-drawer">
          <button class="popup-browser-primary cursor-pointer outline-none regular-fontsize">Browse</button>
          <input class="popup-input regular-fontsize" placeholder="No file selected"/>
        </div>
      </div>
    </div>
    <div class="popup-actions">
      <button class="float-left popup-browser-secondary cursor-pointer outline-none regular-fontsize">Close</button>
      <button class="popup-browser-primary float-right cursor-pointer outline-none regular-fontsize">Update</button>
    </div>    
  </div>
</template>

<script>

export default {
  name: 'updateWindow'
}
</script>
