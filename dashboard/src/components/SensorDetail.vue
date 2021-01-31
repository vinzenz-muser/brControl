<template>
    <div class="sensor">
        <card>
            <span slot="header">
                <h3 class="card-title"> {{ sensor.name }} </h3>
                <h5 class="card-subtitle">ID: {{ sensor.id }}</h5>

                <base-button v-if="sensor.type == 'controller'" class="position-absolute abs-right-button" size="sm" icon type="primary" @click="modalActive = true" :disabled="!active">
                    <i class="tim-icons icon-pencil"></i>
                </base-button>
            </span>

            <div class="sensor-info mb-4">
                <p>Type: {{ sensor.type }}</p>
                <div v-if="sensor.type == 'controller'">
                    <p v-if="!(sensor.target === null)">Target Value: {{ sensor.target }}</p>
                    <p v-else>Target Value: No Data</p>
                    <p v-if="!(sensor.accuracy === null)">Accuracy: {{ sensor.accuracy }}</p>
                    <p v-else>Accuracy: No Data</p>
                </div>
                <p v-if="sensor.lastValue">Current Value: {{ sensor.lastValue | round }}{{ sensor.suffix }}</p>
                <p v-else>Current Value: No Data</p>
                <p v-if="sensor.lastTime">Updated: {{ sensor.lastTime}} </p>
                <p v-else>Updated: No Data</p>
            </div>
            <div class="chart-container">
                <div class="text-right mb-2">
                    <base-button size="sm" type="secondary" v-for="period in periods" @click="updatePlot(period)">{{ period }}</base-button>
                </div>
                <line-chart style="height: 100%"
                    :chart-data="purpleLineChart.chartData"
                    :extra-options="purpleLineChart.extraOptions">
                </line-chart>
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
    import LineChart from '@/components/Charts/LineChart'

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
            return {
                periods: ["1m", "1h", "1d"],
                modalActive: false,
                target: this.sensor.target,
                accuracy: this.sensor.accuracy,
                activeData: "1m",
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
        computed: {
            purpleLineChart: function() {
                return {
                    extraOptions: {
                        maintainAspectRatio: false,
                        legend: {
                            display: false
                        },
                        responsive: true,
                        tooltips: {
                            backgroundColor: '#f5f5f5',
                            titleFontColor: '#333',
                            bodyFontColor: '#666',
                            bodySpacing: 4,
                            xPadding: 12,
                            mode: 'nearest',
                            intersect: 0,
                            position: 'nearest'
                        },
                        scales: {
                            yAxes: [
                                {
                                    gridLines: {
                                    drawBorder: false,
                                    zeroLineColor: 'transparent'
                                    },
                                    ticks: {
                                        padding: 5,
                                    }
                                }
                            ],
                            xAxes: [
                                {
                                    barPercentage: 1.6,
                                    gridLines: {
                                        drawBorder: false,
                                        zeroLineColor: 'transparent'
                                    },
                                    ticks: {
                                        padding: 2,
                                    }
                                }
                            ]
                        }
                    },
                    chartData: {
                        labels: this.sensor.plot_data[this.activeData].timestamps,
                        datasets: [
                            {
                                spanGaps: true,                        
                                fill: true,
                                borderColor: '#d048b6',
                                borderWidth: 2,
                                borderDash: [],
                                borderDashOffset: 0.0,
                                pointBackgroundColor: '#d048b6',
                                pointBorderColor: 'rgba(255,255,255,0)',
                                pointHoverBackgroundColor: '#d048b6',
                                pointBorderWidth: 20,
                                pointHoverRadius: 4,
                                pointHoverBorderWidth: 15,
                                pointRadius: 4,
                                data: this.sensor.plot_data[this.activeData].values,
                            }
                        ]
                    }
                }
            }
        },
        components: {
            Modal,
            LineChart,
        },
        methods: {
            onSubmit () {
                this.$socket.emit('set_targets', {
                    "device_id": this.deviceId,
                    "sensor_id": this.sensor.id,
                    "value": this.target,
                    "accuracy": this.accuracy
                })
                this.modalActive = false;
            },
            updatePlot (period) {
                this.activeData = period
            }
        }
    };
</script>
<style></style>