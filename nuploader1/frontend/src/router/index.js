import Vue from 'vue'
import VueRouter from 'vue-router'
import CompositeList from "../components/CompositeList";

Vue.use(VueRouter)

const routes = [
  {
    path: '/home/:path(.*)',
    name: 'home',
    component: CompositeList,
    props: true,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
