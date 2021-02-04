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
            let date = new Date();
            let minutes =  date.getMinutes()
            let seconds =  date.getSeconds()
            let hours = date.getHours()
            let dateString = (hours < 10 ? '0' : '') + hours  + ":" + (minutes < 10 ? '0' : '') + minutes + ":" + (seconds < 10 ? '0' : '') + seconds

            if (data.device_id in state.devices) {
                Vue.set(state.devices[data.device_id], "active", true)
                if (data.sensor_id in state.devices[data.device_id].sensors) {
                    Vue.set(state.devices[data.device_id].sensors[data.sensor_id], "lastValue", data["value"])
                    Vue.set(state.devices[data.device_id].sensors[data.sensor_id], "lastTime", dateString)
                    if ("1m" in data) {
                        Vue.set(state.devices[data.device_id].sensors[data.sensor_id].plot_data["1m"], "values", data["1m"]["values"])
                        Vue.set(state.devices[data.device_id].sensors[data.sensor_id].plot_data["1m"], "timestamps", data["1m"]["times"])
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
        "SOCKET_update_plot_data"(state, data) {
            for (let plot_values in data['data']) {
                Vue.set(state.devices[data.device_id].sensors[data.sensor_id].plot_data, plot_values, {
                        "timestamps": data['data'][plot_values].timestamps,
                        "values": data['data'][plot_values].values
                    }
                )
            }
        },
        "SOCKET_update_sensor"(state, data) {
            let sensor_id = data['id'];
            let device_id = data['deviceId'];
            Vue.set(state.devices[device_id].sensors[sensor_id], "target", data["target"])
            Vue.set(state.devices[device_id].sensors[sensor_id], "accuracy", data["accuracy"])
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