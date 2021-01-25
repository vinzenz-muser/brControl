<template>
  <div>
    <div class="row">
      <div class="col-lg-12">
          <h1> Devices </h1>
          <card>
            <div class="row">
              <div class="col-sm-12">
                <base-table :data="devices">
                            <template slot="columns">
                            <th class="text-left">#</th>
                            <th>Name</th>
                            <th>Location</th>
                            <th>Connection</th>
                            <th class="text-center"></th>
                          </template>  
                          <template slot-scope="{row}">
                            <td>{{row.id}}</td>
                            <td>{{row.device}}</td>
                            <td>{{row.location}}</td>
                            <td>
                              <badge type="success" v-if="row.active">{{$t('devices.active')}}</badge>
                              <badge type="default" v-else>{{$t('devices.inactive')}}</badge>
                            </td>
                            <td class="td-actions text-right">
                            <router-link :to="{ name: 'controlDeviceDetail', params: { id: row.id }}">
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
        return this.$store.state.devices
      },
      devices() {
        let ans = [];
        for (const [index, device] of Object.entries(this.allDevices)) {
          ans.push(device);
        }
        return ans
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

    },
    watch: {

    },
    methods: {
    }
  };
</script>
<style>
</style>
