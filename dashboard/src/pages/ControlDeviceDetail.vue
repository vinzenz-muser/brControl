<template>
    <ValidationObserver v-slot="{ handleSubmit }">
        <div class="row">
            <div class="col-lg-10">
                <h1>Control Details</h1>
            </div>
            <div class="col-lg-2">
                <base-button size="sm" type="primary" v-on:click="$router.go(-1)">Go Back</base-button>
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
                                    Connection:
                                    <h4 v-if="activeDevice.active">
                                        online
                                    </h4>
                                    <h4 v-else>
                                        offline
                                    </h4>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-lg-12">
                                <h3>
                                    Controllers
                                </h3>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <div class="col-lg-2">
                                Id
                            </div>
                            <div class="col-lg-2">
                                Name
                            </div>
                            <div class="col-lg-2">
                                Last known target
                            </div>
                            <div class="col-lg-2">
                                Last known accuracy
                            </div>
                        </div>
                        <div class="row mb-3" v-for="(sensor, index) in activeDevice.sensors">
                            <div class="col-lg-2">
                                <h5>{{ sensor.id }}</h5>
                            </div>
                            <div class="col-lg-2">
                                <h5>{{ sensor.name }}</h5>
                            </div>
                            <div class="col-lg-2">
                                <h5 v-if="sensor.target">{{ sensor.target }}</h5>
                                <h5 v-else>No Data</h5>
                            </div>
                            <div class="col-lg-2">
                                <h5 v-if="sensor.accuracy">{{ sensor.accuracy }}</h5>
                                <h5 v-else>No Data</h5>
                            </div>
                            <div class="col-lg-2">
                                <div class="text-right">
                                    <div>
                                        <base-button size="sm" icon type="primary" @click="activateSensor(index)">
                                            <i class="tim-icons icon-pencil"></i>
                                        </base-button>
                                        <modal :show="modals[index]" body-classes="p-0">
                                            <card type="secondary"
                                            header-classes="bg-white pb-5"
                                            body-classes="px-lg-5 py-lg-5"
                                            class="border-0 mb-0">
                                                <div>
                                                    <ValidationObserver v-slot="{ handleSubmit }">
                                                        <form class="form-horizontal"
                                                        @submit.prevent="handleSubmit(onSubmit(sensor, index))">
                                                            <span slot="header">
                                                            Change temperatures of
                                                            </span>
                                                            <h2 class="card-title mb-4">{{ sensor.name }}</h2>
                                                            <h4 class="card-title">Target temperature:</h4>
                                                            <ValidationProvider name="Temperature"
                                                            rules="required|min_value:0|max_value:100"
                                                            v-slot="{ passed, failed, errors }">
                                                                <base-input v-model="targettemps[index]" :error="errors[0]"
                                                                :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
                                                                <small slot="helperText" id="emailHelp"
                                                                class="form-text text-muted">Choose the target
                                                                temperature between
                                                                0 and 100 degrees.</small>
                                                                </base-input>
                                                            </ValidationProvider>
                                                            <h4 class="card-title">Accuracy:</h4>
                                                            <ValidationProvider name="Accuracy"
                                                            rules="required|min_value:1|max_value:10"
                                                            v-slot="{ passed, failed, errors }">
                                                                <base-input v-model="targetaccuracies[index]" :error="errors[0]"
                                                                :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
                                                                <small slot="helperText" id="emailHelp"
                                                                class="form-text text-muted">Choose the target
                                                                accuracy between 1
                                                                and 10 degrees.</small>
                                                                </base-input>
                                                            </ValidationProvider>
                                                            <base-button type="secondary" @click="deactivateSensor(index)">Close</base-button>
                                                            <base-button native-type="onSubmit" @act type="primary">Save</base-button>
                                                        </form>
                                                    </ValidationObserver>
                                                </div>
                                            </card>
                                        </modal>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
            <div class="col-sm-12">

            </div>
        </div>
    </ValidationObserver>
</template>
<script>
    import Vue from "vue"
    import { DatePicker, TimeSelect, For, Table, TableColumn } from 'element-ui'
    import { BaseInput, BaseButton, BaseTable, Modal } from '@/components';
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
                console.log(this.targettemps)
                console.log(this.targetaccuracies)
            }
        },
        methods: {
            activateSensor(index) {
                Vue.set(this.modals, index, true)
            },
            deactivateSensor(index) {
                Vue.set(this.modals, index, false)
            },
            onSubmit(sensor, index) {
                this.$socket.emit('update_controller', {
                    "device_id": this.activeDevice.id,
                    "sensor_id": sensor.id,
                    "value": this.targettemps[index],
                    "accuracy": this.targetaccuracies[index]
                })
                this.deactivateSensor(index)
            }
        }
    };
</script>
<style>
</style>