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
              <h5 v-if="device.sensors[device.activeSensor].lastValue" class="card-subtitle mb-2 text-muted">Time: {{ device.sensors[device.activeSensor].lastTime }}</h5>
              
            </div>
            <div class="col-sm-6 d-flex d-sm-block">
              <div class="btn-group btn-group-toggle float-right" data-toggle="buttons">
                <label
                  v-for="(sensor, sensorIndex, i) in device.sensors"
                  :key="sensor.name"
                  class="btn btn-sm btn-primary btn-simple"
                  :class="{ active: device.activeSensor === sensor.id }"
                >
                    <input
                      type="radio"
                      @click="activateSensor(deviceIndex, sensor.id)"
                      name="options"
                      autocomplete="off"
                      :checked="device.activeSensor === sensor.id"
                    />
                    <span class="d-none d-sm-block">{{ i + 1 | roman }}</span>
                </label>
              </div>
            </div>
            <div class="card-body text-center">
              <h1 v-if="device.sensors[device.activeSensor].lastValue" class="title">{{ device.sensors[device.activeSensor].lastValue | round }}°C</h1>
              <h1 v-else class="title">No value</h1>
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
            let firstSensorId = Object.keys(this.devices[device]["sensors"])[0]
            Vue.set(ans, device, this.devices[device])
            Vue.set(ans[device], "activeSensor", parseInt(firstSensorId))
          }
        }

        return ans
      }
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
