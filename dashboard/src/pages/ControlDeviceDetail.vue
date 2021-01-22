<template>
    <div>    
        <div class="row">
            <div class="col-8">
                <h1>Control Device Details</h1>
            </div>
            <div class="col-4">
                <base-button size="sm" class="float-right" type="primary" v-on:click="$router.go(-1)">Go Back</base-button>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-12">
                <div class="card">

                    <div class="card-body">
                        <div class="row">
                            <div class="col-lg-12">
                                <h3>
                                    Basic information
                                </h3>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-lg-5 col-sm-12">
                                <div>
                                    Name:
                                    <h4>
                                        {{ activeDevice.device }}
                                    </h4>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-lg-5 col-sm-12">
                                <div>
                                    Location:
                                    <h4>
                                        {{ activeDevice.location }}
                                    </h4>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-lg-5 col-sm-12">
                                <div>
                                    Connection:<br>
                                    <badge type="success" v-if="activeDevice.active">{{$t('devices.active')}}</badge>
                                    <badge type="default" v-else>{{$t('devices.inactive')}}</badge>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-12">
                <h2>Controllers</h2>
            </div>
        </div>
        <base-alert type="danger" v-if="!activeDevice.active">
        <strong>Attention!</strong> This is device is not connected and therefore you will not be able to change the target values and accuracies of the controllers.        </base-alert>
        <div class="row">
            <div class="col-lg-6 col-sm-12" v-for="(sensor, index) in activeDevice.sensors" v-bind:key="index">
                <sensor-detail :sensor="sensor" :deviceId="activeDevice.id" :active="activeDevice.active"></sensor-detail>
            </div>
        </div>
    </div>
</template>
<script>
import Vue from "vue"
import { DatePicker, TimeSelect, For, Table, TableColumn } from 'element-ui'
import { BaseInput, BaseButton, BaseTable, Modal, SensorDetail, BaseAlert } from '@/components';
import { extend } from "vee-validate";

import {
    required,
    min,
    max,
    min_value,
    max_value
} from "vee-validate/dist/rules";


extend("required", required);
extend("min", min);
extend("max", max);
extend("min_value", min_value);
extend("max_value", max_value);

export default {
    props: ['id'],
    name: "ControlDeviceDetail",
    data() {
        return {
            targettemps: [],
            targetaccuracies: [],
            active: false,
            modals: [],
        }
    },
    components: {
        [DatePicker.name]: DatePicker,
        [TimeSelect.name]: TimeSelect,
        [Table.name]: Table,
        [TableColumn.name]: TableColumn,
        BaseInput,
        BaseButton,
        BaseTable,
        Modal,
        SensorDetail,
        BaseAlert
    },
    computed: {
        allDevices() {
            let devices = this.$store.state.devices
            return devices
        },
        activeDevice() {
            let _this = this;
            let ans = {};
            for (const [index, device] of Object.entries(this.allDevices)) {
                if (_this.id == device.id) {
                    ans = device;
                }
            }

            return ans;
        }
    },
    watch: {
        activeDevice() {
            this.modals.splice(0)
            this.targettemps.splice(0)
            this.targetaccuracies.splice(0)

            for (const sensor in this.activeDevice.sensors) {
                let current_sens = this.activeDevice.sensors[sensor]
                this.modals.push(false);
                this.targettemps.push(current_sens.target)
                this.targetaccuracies.push(current_sens.accuracy)
            }
        }
    },
    methods: {
    }
};
</script>
<style>
</style>