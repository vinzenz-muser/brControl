import Vue from 'vue'
import Vuex from 'vuex'
import router from "./routes/router"
import { StatsCard } from './components'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        devices: {}
    },
    getters: {
    },
    mutations: {
        "SOCKET_new_data"(state, data) {
            Vue.set(state.devices[data.deviceid], "active", true)
            let sensorid = 0;
            let date = new Date();
            let dateString = date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()

            for (sensorid in data.data) {
                for (let sensorindex in state.devices[data.deviceid].sensors) {
                    if (state.devices[data.deviceid].sensors[sensorindex].id === parseInt(sensorid)) {
                        Vue.set(state.devices[data.deviceid].sensors[sensorindex], "lastValue", data.data[sensorid])
                        Vue.set(state.devices[data.deviceid].sensors[sensorindex], "lastTime", dateString)
                    }
                }
            }
        },
        "SOCKET_device_disconnect"(state, data) {
            let id = data["id"]
            Vue.set(state.devices[id], "active", false)
        },
        "SOCKET_update_sensors"(state, data) {
            state.devices = data
        },
        "SOCKET_login_successful"(state, data) {
            localStorage.email = data["email"]
            localStorage.token = data["token"]
            localStorage.name = data["name"]
            this._vm.$socket.emit('update_sensors')
            if (router.history.current.path == "/login") {
                router.push({ name: 'dashboard' })
            }
        },
        "SOCKET_login_failed"(state, data) {
            alert("Login failed")
        },
        "SOCKET_token_login_failed"(state, data) {
            console.log("Token Login failed")
        },
        "SOCKET_connect"(state) {
            if (localStorage.token != "") {
                this._vm.$socket.emit('login_token', { "token": localStorage.token })
            } else {
                router.push({ name: 'login' })
            }
        },
        "SOCKET_logged_out"(state) {
            localStorage.email = ""
            localStorage.token = ""
            localStorage.name = ""
            router.push({ name: 'login' })
        },
        "activate_sensor"(state, indices) {
            state.activeDevices[indices[0]]["activeSensor"] = indices[1]
        }
    },
    actions: {},
    getters: {}
})