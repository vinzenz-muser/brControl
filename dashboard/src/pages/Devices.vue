<template>
  <div>
    <div class="row">
      <div class="col-lg-12"  v-for="(device, index) in allDevices" :key="index">
          <card>
          <div class="row">
            <div class="col-sm-6">
              <h3 class="card-title">{{ device.Device }}</h3>
              <h4 class="card-subtitle">{{ device.Location }}</h4>
              <router-link :to="{ name: 'deviceDetail', params: { name: device.Device }}">{{ $t('devices.showhistory') }}</router-link>
            </div>
            <div class="col-sm-6 d-flex d-sm-block">
              <div class="btn-group btn-group-toggle float-right">
                <badge type="info" v-if="activeIndicator[device.ID]">{{$t('devices.active')}}</badge>   
              </div>   
            </div>
          </div>
        </card>
      </div>
    </div>
  </div>
</template>
<script>
  import Vue from "vue"
  export default {
    computed: {
      allDevices () {
        return this.$store.state.allDevices
      },
      activeDevices () {
        return this.$store.state.activeDevices
      },
      activeIndicator () {
        let ans = {};
        let device;
        for (const [index, device] of Object.entries(this.allDevices)) {
          ans[device.ID] = device.ID in this.activeDevices;
        }
        return ans;
      }
    },
    created() {
      this.$socket.emit('update_sensors')
    },
    watch: {

    },
    methods: {
    }
  };
</script>
<style>
</style>
