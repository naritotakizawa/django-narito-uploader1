import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'

const getCookie = name => {
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const [key, value] = cookie.trim().split('=')
            if (key === name) {
                return decodeURIComponent(value)
            }
        }
    }
}

Vue.config.productionTip = false

Vue.prototype.$http = (url, opts) => fetch(url, opts)
Vue.prototype.$csrfToken = getCookie('csrftoken')
Vue.prototype.$endpoint = process.env.NODE_ENV === 'production' ?  '/uploader/api/composites/'  : 'http://127.0.0.1:8000/uploader/api/composites/'
Vue.prototype.$fileUrlBase = process.env.NODE_ENV === 'production' ?  '/uploader'  : 'http://127.0.0.1:8000/uploader'
Vue.prototype.$zipUrlBase = process.env.NODE_ENV === 'production' ?  '/uploader/zip/'  : 'http://127.0.0.1:8000/uploader/zip/'


new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
