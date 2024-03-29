import Vue from 'vue';
import Router from 'vue-router';
import DefaultLayout from '../layout/DefaultLayout.vue';
import AuthLayout from '../layout/AuthLayout.vue';
import Dashboard from '../pages/Dashboard.vue'
import Devices from '../pages/Devices.vue'
import NotFound from '../pages/NotFound.vue'
import Login from '../pages/Login.vue'
import DeviceDetail from '../pages/DeviceDetail.vue'

Vue.use(Router);

Vue.prototype.assetPath = '/static/dash';

let authPages = {

};

export default new Router({
  routes: [
    {
      path: '/',
      name: '',
      component: DefaultLayout,
      redirect: "/dashboard",
      children: [
        {
          path: '/dashboard',
          name: 'dashboard',
          component: Dashboard,
          props: {}
        },
        {
          path: '/devices',
          name: 'devices',
          component: Devices,
          props: {}
        },
        {
          path: '/device/:id',
          name: 'deviceDetail',
          component: DeviceDetail,
          props: true
        }
      ]
    },
    {
      path: '/', 
      name: 'authlayout',
      component: AuthLayout,
      children: [
        {
          path: 'login',
          name: 'login',
          component: Login,
          props: {}
        },
        {
          path: '*',
          name: 'notfound',
          component: NotFound,
          props: {}
        }
      ]
    }
  ]
});