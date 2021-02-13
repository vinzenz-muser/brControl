<template>
    <router-link :to="{ name: 'deviceDetail', params: { id: device.id }}">
        <card>
            <template slot="default">
                <div class="container">
                    <div class="row">
                        <div class="col-lg-9">
                            <h3 class="card-title"> {{ device.device }}</h3>  
                            <h5 class="card-subtitle mb-2 text-muted">Location: {{ device.location }}</h5>
                            <h5 class="card-subtitle mb-2 text-muted">Sensors: {{ Object.keys(device.sensors).length }}</h5>

                        </div>
                        <div class="col-lg-3">
                            <div class="mt-1">
                                <badge v-if="device.active" class="float-right" type="success">Online</badge>
                                <badge v-else="device.active" class="float-right" type="info">Offline</badge>
                            </div>
                        </div>
                    </div>
                </div>
            </template>
        </card>
    </router-link>    
</template>
<script>
    export default {
        name: "device-card-list",
        props: ["device"],
        data () {
            console.log(this.device)
            return {
                activeSensor: parseInt(Object.keys(this.device["sensors"])[0])
            }
        }
    };
</script>
<style></style>