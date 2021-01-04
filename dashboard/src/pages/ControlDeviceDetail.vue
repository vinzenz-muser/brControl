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
                    <div class="card-header card-header-primary">
                        <h3 class="card-title">Information</h3>
                        <p class="card-category"></p>
                    </div>
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

                        <div class="row mt-4">
                            <div class="col-lg-12">
                                <h3>
                                    Controllers
                                </h3>
                            </div>
                        </div>
                        <div>
                            <div class="col-lg-12 col-sm-12">
                                <div>
                                    <el-table class="table-striped" :data="activeDevice.sensors">
                                        <el-table-column type="index">
                                        </el-table-column>
                                        <el-table-column prop="name" label="Name">
                                        </el-table-column>
                                        <el-table-column label="Active">
                                        </el-table-column>
                                        <el-table-column label="Last known target">
                                        </el-table-column>
                                        <el-table-column label="Last known accuracy">
                                        </el-table-column>
                                        <el-table-column :open-delay="300" placement="top" max-width="50">
                                            <base-button type="info" size="sm" icon>
                                                <i class="tim-icons icon-pencil"></i>
                                            </base-button>
                                        </el-table-column>
                                    </el-table>
                                    </h4>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-12">
                <form class="form-horizontal" @submit.prevent="handleSubmit(submit)">
                    <card type="danger" class="card-success">
                        <span slot="header">
                            Change temperatures
                        </span>
                        <h2 class="card-title mb-4">Change the target temperature of the device</h2>
                        <h4 class="card-title">Target temperature:</h4>
                        <ValidationProvider name="Temperature" rules="required|min_value:0|max_value:100"
                            v-slot="{ passed, failed, errors }">
                            <base-input v-model="targettemp" :error="errors[0]"
                                :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
                                <small slot="helperText" id="emailHelp" class="form-text text-muted">Choose the target
                                    temperature between
                                    0 and 100 degrees.</small>
                            </base-input>
                        </ValidationProvider>
                        <h4 class="card-title">Accuracy:</h4>
                        <ValidationProvider name="Accuracy" rules="required|min_value:1|max_value:10"
                            v-slot="{ passed, failed, errors }">
                            <base-input v-model="targetaccuracy" :error="errors[0]"
                                :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
                                <small slot="helperText" id="emailHelp" class="form-text text-muted">Choose the target
                                    accuracy between 1
                                    and 10 degrees.</small>
                            </base-input>
                        </ValidationProvider>
                        <base-button native-type="submit" type="primary">Update configuration</base-button>
                    </card>
                </form>
            </div>
        </div>
    </ValidationObserver>
</template>
<script>
    import Vue from "vue"
    import { DatePicker, TimeSelect, For, Table, TableColumn } from 'element-ui'
    import { BaseInput, BaseButton, BaseTable } from '@/components';
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
                targettemp: "",
                targetaccuracy: "",
                active: false,
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
        },
        computed: {
            allDevices() {
                return this.$store.state.devices
            },
            activeDevice() {
                let _this = this;
                let ans = {};
                for (const [index, device] of Object.entries(this.allDevices)) {
                    if (_this.id == device.id) {
                        ans = device;
                    }
                }
                console.log(ans)
                return ans;
            }
        },
        watch: {
            allDevices() {
                this.updateActiveDevice()
            }
        },
        methods: {
            updateActiveDevice() {

            },
            submit() {
                alert("Form has been submitted!");
            }
        }
    };
</script>
<style>
</style>