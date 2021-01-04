/<template>
  <div>
    <div class="row">
      <div class="col-lg-6" v-for="(device, deviceIndex) in activeDevices" :key="deviceIndex">
        <card>
        <template slot="header">
          <div class="row">
            <div class="col-sm-6">
              <h3 class="card-title"> {{ device.device }} </h3>
              <h5 class="card-subtitle mb-2 text-muted">Location: {{ device.location }}</h5>
              <h5 class="card-subtitle mb-2 text-muted">Sensor: {{ device.sensors[device.activeSensor].name }}</h5>
              <h5 class="card-subtitle mb-2 text-muted">Value of: {{ device.sensors[device.activeSensor].lastTime }}</h5>
              
            </div>
            <div class="col-sm-6 d-flex d-sm-block">
              <div class="btn-group btn-group-toggle float-right" data-toggle="buttons">
                <label
                  v-for="(sensor, sensorIndex) in device.sensors"
                  :key="sensor.name"
                  class="btn btn-sm btn-primary btn-simple"
                  :class="{ active: device.activeSensor === sensorIndex }"
                >
                    <input
                      type="radio"
                      @click="activateSensor(deviceIndex, sensorIndex)"
                      name="options"
                      autocomplete="off"
                      :checked="device.activeSensor === sensorIndex"
                    />
                    <span class="d-none d-sm-block">{{ sensorIndex + 1 | roman }}</span>
                </label>
              </div>
            </div>
            <div class="card-body text-center">
              <h1 class="title">{{ device.sensors[device.activeSensor].lastValue | round }}°C</h1>
            </div>
          </div>
        </template>
        </card>
      </div>
    </div>
  </div>
</template>
<script>
  import Vue from "vue"
  export default {
    computed: {
      devices () {
        return this.$store.state.devices
      },
      activeDevices () {
        let ans = {};

        for (let device in this.devices) {
          if (this.devices[device].active) {
            Vue.set(ans, device,this.devices[device])
            Vue.set(ans[device], "activeSensor", 0)
          }
        }

        return ans
      }
    },
    methods: {
      activateSensor(deviceId, sensorIndex) {
        Vue.set(this.activeDevices[deviceId], "activeSensor", sensorIndex)
      }
    },
    filters: {
      round (value) {
        return Math.round(value * 10) / 10
      },
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
