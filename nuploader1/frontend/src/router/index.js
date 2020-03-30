import Vue from 'vue'
import VueRouter from 'vue-router'
import CompositeList from '../components/CompositeList'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: CompositeList,
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
