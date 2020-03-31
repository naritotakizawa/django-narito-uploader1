import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

Vue.prototype.$http = (url, opts) => fetch(url, opts)
Vue.prototype.$endpoint = 'http://127.0.0.1:8000/uploader/api/composites/'

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
