import Vue from 'vue'
import Vuex from 'vuex'
import router from "./routes/router"
import { StatsCard } from './components'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    activeDevices: {},
    allDevices: {},
  },
  getters: {
  },
  mutations: {
    "SOCKET_new_data" (state, data) { 
      for (let [id, device] of Object.entries(data)) {
        if (!state.activeDevices.hasOwnProperty(device["ID"])) {
          let first_device = Object.keys(device.Data)[0];
          Vue.set(state.activeDevices, device["ID"], device);
          Vue.set(state.activeDevices[device["ID"]], "activeSensor", first_device)
        } else {
          state.activeDevices[device["ID"]]["Data"] = device.Data
        }
      }
    },
    "SOCKET_sensor_remove" (state, data) {
      let id = data["ID"]

      if (Object.keys(state.activeDevices).includes(id)) {
        Vue.delete(state.activeDevices, id)
      }
    },
    "SOCKET_sensor_history_update" (state, data) {
      for (let [key, value] of Object.entries(data)) {
        if (!state.allDevices.hasOwnProperty(key)) {
          Vue.set(state.allDevices, key, value);
        }
      }
    },
    "SOCKET_login_successful" (state, data) {
      localStorage.email = data["email"]
      localStorage.token = data["token"]
      localStorage.name = data["name"]
      if (router.history.current.path == "/login") {
        router.push({ name: 'dashboard' })
      }
    },
    "SOCKET_login_failed" (state, data) {
      alert("Login failed")
    },
    "SOCKET_token_login_failed" (state, data) {
      console.log("Token Login failed")
    },
    "SOCKET_connect" (state) {
      if (localStorage.token != "") {
        this._vm.$socket.emit('login_token', {"token": localStorage.token})
      } else {
        router.push({ name: 'login' })
      }
    },
    "SOCKET_logged_out" (state) {
      localStorage.email = ""
      localStorage.token = ""
      localStorage.name = ""
      router.push({ name: 'login' })
    },
    "activate_sensor" (state, indices) {
      state.activeDevices[indices[0]]["activeSensor"] = indices[1]
    }
  },
  actions: {},
  getters: {}
})