<template>
  <div>
    <div class="row">
      <div class="col-lg-6" v-for="(device, deviceIndex) in activeDevices" :key="deviceIndex">
        <card>
        <template slot="header">
          <div class="row">
            <div class="col-sm-6">
              <h3 class="card-title"> {{ device.Device }} </h3>
              <h5 class="card-subtitle mb-2 text-muted">Location: {{ device.Location }}</h5>
              <h5 class="card-subtitle mb-2 text-muted">Sensor: {{ device.activeSensor }}</h5>
              
            </div>
            <div class="col-sm-6 d-flex d-sm-block">
              <div class="btn-group btn-group-toggle float-right" data-toggle="buttons">
                <label
                  v-for="(sensor, sensorIndex, number) in device.Data"
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
                    <span class="d-none d-sm-block">{{ number + 1 | roman }}</span>
                </label>
              </div>
            </div>
            <div class="card-body text-center">
              <h1 class="title">{{ device.Data[device.activeSensor] | round }}°C</h1>
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
      activeDevices () {
        return this.$store.state.activeDevices
      },
    },
    methods: {
      activateSensor(sensorIndex, tempIndex) {
        this.$store.commit("activate_sensor", [sensorIndex, tempIndex])
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
