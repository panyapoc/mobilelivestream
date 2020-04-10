import Vue from "vue";
import App from "./App.vue";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import VueClipboard from 'vue-clipboard2'
import axios from "axios";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(VueClipboard);
Vue.prototype.$http = axios;

Vue.config.productionTip = false;

new Vue({
  render: h => h(App)
}).$mount("#app");
