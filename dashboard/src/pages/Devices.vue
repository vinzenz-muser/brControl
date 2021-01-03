<template>
  <div>
    <div class="row">
      <div class="col-lg-12">
          <h1> Sensor devices </h1>
          <card>
            <div class="row">
              <div class="col-sm-12">
                <base-table :data="sensorDevices">
                            <template slot="columns">
                            <th class="text-left">#</th>
                            <th>Name</th>
                            <th>Location</th>
                            <th>Active</th>
                            <th class="text-center"></th>
                          </template>  
                          <template slot-scope="{row}">
                            <td>{{row.ID}}</td>
                            <td>{{row.Device}}</td>
                            <td>{{row.Location}}</td>
                            <td>
                              <badge type="success" v-if="activeIndicator[row.ID]">{{$t('devices.active')}}</badge>
                              <badge type="default" v-else>{{$t('devices.inactive')}}</badge>
                            </td>
                            <td class="td-actions text-right">
                            <router-link :to="{ name: 'deviceDetail', params: { id: row.ID }}">
                                <base-button type="success" size="sm" icon>
                                  <i class="tim-icons icon-zoom-split"></i>
                                </base-button>
                              </router-link>
                            </td>
                          </template>    
                </base-table>
              </div>
            </div>
          </card>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12">
          <h1> Control devices </h1>
          <card>
            <div class="row">
              <div class="col-sm-12">
                <base-table :data="controlDevices">
                            <template slot="columns">
                            <th class="text-left">#</th>
                            <th>Name</th>
                            <th>Location</th>
                            <th>Active</th>
                            <th class="text-center"></th>
                          </template>  
                          <template slot-scope="{row}">
                            <td>{{row.ID}}</td>
                            <td>{{row.Device}}</td>
                            <td>{{row.Location}}</td>
                            <td>
                              <badge type="success" v-if="activeIndicator[row.ID]">{{$t('devices.active')}}</badge>
                              <badge type="default" v-else>{{$t('devices.inactive')}}</badge>
                            </td>
                            <td class="td-actions text-right">
                            <router-link :to="{ name: 'controlDeviceDetail', params: { id: row.ID }}">
                                <base-button type="success" size="sm" icon>
                                  <i class="tim-icons icon-zoom-split"></i>
                                </base-button>
                              </router-link>
                            </td>
                          </template>    
                </base-table>
              </div>
            </div>
          </card>
      </div>
    </div>
  </div>
</template>
<script>
  import Vue from "vue"
  import { BaseTable } from '@/components';
  export default {
     components: {
      BaseTable,
    },
    props: ['id'],
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
      },
      controlDevices() {
        let ans = [];
        for (const [index, device] of Object.entries(this.allDevices)) {
          if (device.Type == "control") {
            ans.push(device);
          }
        }
        return ans
      },
      sensorDevices() {
        let ans = [];
        for (const [index, device] of Object.entries(this.allDevices)) {
          if (device.Type == "sensors") {
            ans.push(device);
          }
        }

        return ans
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
