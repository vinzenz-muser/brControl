<template>
    <div class="device-card">
        <card>
            <template slot="header">
              <div>
                <div>
                  <h3 class="card-title">                   
                    <router-link :to="{ name: 'deviceDetail', params: { id: device.id }}">
                      {{ device.device }} 
                    </router-link>  
                  </h3>  
                  <h5 class="card-subtitle mb-2 text-muted">Location: {{ device.location }}</h5>
                  <h5 class="card-subtitle mb-2 text-muted">Sensor: {{ device.sensors[activeSensor].name }}</h5>
                  <h5 v-if="device.sensors[activeSensor].lastValue" class="card-subtitle mb-2 text-muted">Time: {{ device.sensors[activeSensor].lastTime }}</h5>
                </div>
                <div class="d-sm-block">
                  <div class="btn-group btn-group-toggle float-right" data-toggle="buttons" v-if="device.active">
                    <label
                      v-for="(sensor, sensorIndex, i) in device.sensors"
                      :key="sensor.name"
                      class="btn btn-sm btn-primary btn-simple"
                      :class="{ active: activeSensor === sensor.id }"
                    >
                        <input
                          type="radio"
                          @click="activateSensor(sensor.id)"
                          name="options"
                          autocomplete="off"
                          :checked="activeSensor === sensor.id"
                        />
                        <span class="d-none d-sm-block">{{ i + 1 | roman }}</span>
                    </label>
                  </div>
                </div>
                <div class="card-body text-center" v-if="device.active">
                  <h1 v-if="device.sensors[activeSensor].lastValue" class="title">{{ device.sensors[activeSensor].lastValue | round }}°C</h1>
                  <h1 v-else class="title">No value</h1>
                </div>
              </div>
            </template>
        </card>
    </div>
</template>
<script>
    export default {
        name: "device-card",
        props: ["device"],
        data () {
            return {
                activeSensor: parseInt(Object.keys(this.device["sensors"])[0])
            }
        },
        methods: {
            activateSensor(sensorId) {
                this.activeSensor = sensorId
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
<style></style>