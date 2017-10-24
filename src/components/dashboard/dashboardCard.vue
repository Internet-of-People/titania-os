<template>
  <div class="clearfix single-events-div ">
    <div class="clearfix events-desc-div">
      <div class="overview-events clearfix">
        <div class="overview-event-count total-servers">4</div>
        <div class="overview-event-desc large-fontsize">{{testProp.drilldownname}}</div>
        <div class="overview-event-icon"></div>
      </div>
      <div class="overview-event-image overview-servers-total"></div>
    </div><div class="overview-events-link-div">
      <span class="overview-events-link-desc regular-fontsize" id="owlinkdesc">{{testProp.caption}}</span>
      <span class="overview-events-link">&#8594</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'dashboardCard',
  props: ['testProp']
}
</script>
