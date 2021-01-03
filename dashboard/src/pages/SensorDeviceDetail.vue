<template>
    <div>
      <div class="row">
        <div class="col-lg-10">
          <h1>Sensor Details</h1>
        </div>
        <div class="col-lg-2">
                <base-button size="sm" type="primary" v-on:click="$router.go(-1)">Go Back</base-button>
        </div>
      </div>
      <div class="row">
        <div class="col-sm-6">
          <base-input>
            <el-date-picker v-model="dateTimePickerFrom"
                            type="datetime"
                            placeholder="Select start">
            </el-date-picker>
          </base-input>
        </div>
        <div class="col-sm-6">
          <base-input>
            <el-date-picker v-model="dateTimePickerTo"
                            type="datetime"
                            placeholder="Select end">
            </el-date-picker>
          </base-input>
        </div>
      </div>
    </div>
</template>
<script>
  import Vue from "vue"
  import {DatePicker, TimeSelect} from 'element-ui'

  export default {
    data() {
      return {
        dateTimePickerFrom: '',
        dateTimePickerTo: ''
      }
    },
    components: {
      [DatePicker.name]: DatePicker,
      [TimeSelect.name]: TimeSelect
    },
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
    watch: {

    },
    methods: {
    }
  };
</script>
<style>
</style>
