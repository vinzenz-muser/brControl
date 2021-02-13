<template>
  <div>
    <div class="row">
      <div class="col-lg-12">
        <h1> Devices </h1>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-6"  v-for="device in devices">
        <device-card-list v-bind:device="device"></device-card-list>
      </div>
    </div>
  </div>
</template>
<script>
  import Vue from "vue"
  import { BaseTable, DeviceCardList } from '@/components';
  export default {
    components: {
      BaseTable,
      DeviceCardList
    },
    props: ['id'],
    computed: {
      allDevices() {
        return this.$store.state.devices
      },
      devices() {
        let ans = [];
        for (const [index, device] of Object.entries(this.allDevices)) {
          ans.push(device);
        }
        return ans
      },
      activeIndicator() {
        let ans = {};
        let device;
        for (const [index, device] of Object.entries(this.allDevices)) {
          ans[device.ID] = device.ID in this.activeDevices;
        }
        return ans;
      }
    },
    created() {

    },
    watch: {

    },
    methods: {
    }
  };
</script>
<style>
</style>