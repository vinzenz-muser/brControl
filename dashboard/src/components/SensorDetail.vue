<template>
    <div class="sensor">
        <card>
            <span slot="header">
                <h3 class="card-title"> {{ sensor.name }} </h3>
                <h5 class="card-subtitle">ID: {{ sensor.id }}</h5>
                <base-button class="position-absolute abs-right-button" size="sm" icon type="primary" @click="modalActive = true" :disabled="!active">
                    <i class="tim-icons icon-pencil"></i>
                </base-button>
            </span>

            <div class="sensor-info">
                <p v-if="!(sensor.target === null)">Target Value: {{ sensor.target }}</p>
                <p v-else>Target Value: No Data</p>
                <p v-if="!(sensor.accuracy === null)">Accuracy: {{ sensor.accuracy }}</p>
                <p v-else>Accuracy: No Data</p>
                <p v-if="sensor.lastValue">Last Value: {{ sensor.lastValue | round }}{{ sensor.suffix }}</p>
                <p v-else>Last Value: No Data</p>
                <p v-if="sensor.lastTime">Last Updated: {{ sensor.lastTime}} </p>
                <p v-else>Last Updated: No Data</p>
            </div>
        </card>
        <modal :show="modalActive" body-classes="p-0">
            <card type="secondary" header-classes="bg-white pb-5" body-classes="px-lg-5 py-lg-5" class="border-0 mb-0">
                <div>
                    <ValidationObserver v-slot="{ handleSubmit }">
                        <form class="form-horizontal" @submit.prevent="handleSubmit(onSubmit)">
                            <span slot="header">
                                Change temperatures of
                            </span>
                            <h2 class="card-title mb-4">{{ sensor.name }}</h2>
                            <h4 class="card-title">Target temperature:</h4>

                            <ValidationProvider 
                                name="Temperature" 
                                rules="required|min_value:0|max_value:100"
                                v-slot="{ passed, failed, errors }">

                                <base-input 
                                    v-model="target" 
                                    :error="errors[0]"
                                    :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
                                    >
                                    <small slot="helperText" id="emailHelp" class="form-text text-muted">Choose the
                                        target
                                        temperature between
                                        0 and 100 degrees.</small>
                                </base-input>

                            </ValidationProvider>

                            <h4 class="card-title">Accuracy:</h4>

                            <ValidationProvider 
                                name="Accuracy" 
                                rules="required|min_value:0.5|max_value:10"
                                v-slot="{ passed, failed, errors }">

                                <base-input 
                                    v-model="accuracy" 
                                    :error="errors[0]"
                                    :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
                                    >
                                    <small slot="helperText" id="emailHelp" class="form-text text-muted">Choose the
                                        target
                                        accuracy between 0.1
                                        and 10 degrees.</small>
                                </base-input>

                            </ValidationProvider>
                            <base-button type="secondary" @click="modalActive = false">Close</base-button>
                            <button type="submit" native-type="submit" class="float-right btn btn-fill btn-success btn-wd">Save</button>
                        </form>
                    </ValidationObserver>
                </div>
            </card>
        </modal>
    </div>

</template>
<script>
    import { extend } from "vee-validate";
    import { BaseInput, BaseButton, BaseTable, Modal, SensorDetail } from '@/components';
    import { configure } from 'vee-validate';

    import {
        required,
        min,
        max,
        min_value,
        max_value
    } from "vee-validate/dist/rules";

    extend("min_value", min_value);
    extend("max_value", max_value);

    export default {
        name: "sensor-detail",
        props: ["sensor", "deviceId", "active"],
        data () {
            console.log(this.sensor)
            return {
                modalActive: false,
                target: this.sensor.target,
                accuracy: this.sensor.accuracy,
                modelValidations: {
                    target: {
                        required: true,
                        email: true
                    },
                    accuracy: {
                        required: true,
                        min: 5
                    }
                }
            }
        },
        watch: {
            sensor () {
                //this.target = this.sensor.target;
                //this.accuracy = this.sensor.accuracy;
            }
        },
        components: {
            Modal
        },
        methods: {
            onSubmit () {
                this.$socket.emit('update_controller', {
                    "device_id": this.deviceId,
                    "sensor_id": this.sensor.id,
                    "value": this.target,
                    "accuracy": this.accuracy
                })
                this.modalActive = false;
            }
        }
    };
</script>
<style></style>