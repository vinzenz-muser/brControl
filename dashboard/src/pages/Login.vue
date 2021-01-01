<template>
  <div class="container">
    <div class="col-lg-4 col-md-6 ml-auto mr-auto">
      <ValidationObserver v-slot="{ handleSubmit }">
        <form @submit.prevent="handleSubmit(submit)">
          <card class="card-login card-white">
            <template slot="header">
              <img v-bind:src="assetPath+'/img/card-primary.png'" alt="" />
              <h1 class="card-title">Log in</h1>
            </template>

            <div>
              <ValidationProvider
                name="Username"
                rules="required"
                v-slot="{ passed, failed, errors }"
              >
              <base-input
                required
                v-model="username"
                type="text"
                placeholder="Username"
                addon-left-icon="tim-icons icon-minimal-right"
                :error="errors[0]"
                :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
              </base-input>
             </ValidationProvider>

             <ValidationProvider
               name="password"
               rules="required|min:5"
               v-slot="{ passed, failed, errors }"
             >
             <base-input
               required
               v-model="password"
               placeholder="Password"
               addon-left-icon="tim-icons icon-lock-circle"
               type="password"
               :error="errors[0]"
               :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
             </base-input>
            </ValidationProvider>
            </div>

            <div slot="footer">
              <base-button native-type="submit" type="primary" class="mb-3" size="lg" block>
              Login
              </base-button>
            </div>
          </card>
        </form>
      </ValidationObserver>
    </div>
  </div>
</template>
<script>

import { extend } from "vee-validate";
import { required, email, min } from "vee-validate/dist/rules";
import sha256 from "js-sha256";
import Vue from "vue"

extend("min", min);
extend("required", required);

export default {
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    submit() {
      // var addpass = sha256(this.password)
      let ans = {
        "username": this.username,
        "password": this.password
      }
      this.$socket.emit('login', ans)
    }
  }
};
</script>
<style>
.navbar-nav .nav-item p {
  line-height: inherit;
  margin-left: 5px;
}
</style>
