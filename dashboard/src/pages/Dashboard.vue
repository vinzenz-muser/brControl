/<template>
  <div>
    <div class="row">
      <div class="col-lg-6" v-for="(device, deviceIndex) in activeDevices" :key="deviceIndex">
        <device-card v-bind:device="device"></device-card>
      </div>
    </div>
  </div>
</template>
<script>
  import Vue from "vue"
  import { DeviceCard } from '@/components';
  export default {
    computed: {
      devices () {
        return this.$store.state.devices
      },
      activeDevices () {
        let ans = {};

        for (let device in this.devices) {
          if (this.devices[device].active) {
            let firstSensorId = Object.keys(this.devices[device]["sensors"])[0]
            Vue.set(ans, device, this.devices[device])
            Vue.set(ans[device], "activeSensor", parseInt(firstSensorId))
          }
        }

        return ans
      }
    },
    components: {
      DeviceCard
    },
    methods: {
      activateSensor(deviceId, sensorId) {
        Vue.set(this.activeDevices[deviceId], "activeSensor", sensorId)
      }
    },
    filters: {
      roman (value) {
        if (value <= 3) {
          let ans = ""
          for (let i=0; i<value; i++) {
            ans += "I"
          }
          return ans
        }
        if (value == 4) {
          return "IV"
        }
        if (value == 5) {
          return "V"
        }
        if (value == 6) {
          return "VI"
        }
        if (value == 7) {
          return "VII"
        }
        if (value == 8) {
          return "VIII"
        }
        if (value == 9) {
          return "IX"
        }
        if (value == 10) {
          return "X"
        }
        return value
      }
    }
  };
</script>
<style>
</style>
