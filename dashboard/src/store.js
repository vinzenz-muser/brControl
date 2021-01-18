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
            let minutes =  date.getMinutes()
            let seconds =  date.getSeconds()
            let hours = date.getHours()
            let dateString = (hours < 10 ? '0' : '') + hours  + ":" + (minutes < 10 ? '0' : '') + minutes + ":" + (seconds < 10 ? '0' : '') + seconds

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
        "SOCKET_update_sensor_values"(state, data) {
            let current_device = state.devices[data["deviceId"]]

            for (const sid in current_device.sensors) {
                if (current_device.sensors[sid].id == data.id) {
                    let current_sensor = current_device.sensors[sid] 
                    for (const key in data) {
                        Vue.set(current_sensor, key, data[key])
                    }
                }
            }
        },
        "SOCKET_login_successful"(state, data) {
            localStorage.name = data["name"]
            this._vm.$socket.emit('update_sensors')
            if (router.history.current.path == "/login") {
                router.push({ name: 'dashboard' })
            }
        },
        "SOCKET_login_failed"(state, data) {
            let location = (window.location + "").split("/")
            let url = location[0] + "//" + location[2] + "/auth/login?next=" + window.location.pathname + window.location.hash
            window.location.replace(url)
        },
        "SOCKET_connect"(state) {
            console.log("Successfully logged in!")
        }
    },
    actions: {},
    getters: {}
})