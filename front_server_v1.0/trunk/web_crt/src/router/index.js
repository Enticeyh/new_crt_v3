import { createRouter, createWebHashHistory } from 'vue-router'
import webCrtIndex from '../views/index.vue'
import statistics from '../views/statistics.vue'
import message from '../views/message.vue'
import compile from '../views/compile.vue'
import systemSet from '../views/systemSet.vue'

const routes = [
//   // 首页
    {
    path: '/',
    name: 'webCrtIndex',
    component: webCrtIndex,
  },
  // 统计查询
  {
    path: '/statistics',
    name: 'statistics',
    component: statistics,
  },
  // 信息查询
  {
    path: '/message',
    name: 'message',
    component: message,
  },
  // 信息编辑
  {
    path: '/compile',
    name: 'compile',
    component: compile,
  },
  // 系统设置
  {
    path: '/systemSet',
    name: 'systemSet',
    component: systemSet,
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
