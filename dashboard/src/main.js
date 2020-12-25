/*!

 =========================================================
 * Vue Black Dashboard PRO - v1.2.3
 =========================================================

 * Product Page: https://www.creative-tim.com/product/vue-black-dashboard-pro
 * Copyright 2019 Creative Tim (https://www.creative-tim.com)

 * Coded by Creative Tim

 =========================================================

 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 */
import Vue from 'vue';
import VueRouter from 'vue-router';
import RouterPrefetch from 'vue-router-prefetch'
import DashboardPlugin from './plugins/dashboard-plugin';
import App from './App.vue';
import VueSocketIO from 'vue-socket.io'
import store from "./store";

// router setup
import router from './routes/router';
import i18n from './i18n';
import './registerServiceWorker'
// plugin setup
Vue.use(DashboardPlugin);
Vue.use(VueRouter);
Vue.use(RouterPrefetch);

var url = window.location.href
var arr = url.split(":");
var domain = arr[1].split("/")[2];
console.log('https://'+domain+':42160/dashboard')
Vue.use(new VueSocketIO({
  debug: false,
  connection: 'https://'+domain+':42160/dashboard',
  vuex: {
    store,
    actionPrefix: "SOCKET_",
    mutationPrefix: "SOCKET_"
  }
}));


/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App),
  router,
  store,
  i18n
});
