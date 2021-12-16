export default [
  { name: 'Dashboard', path: '/', component: () => import('../pages/Index.vue') },
  { name: 'Clients', path: '/clients', component: () => import('../pages/Clients.vue') },
  { name: 'Register', path: '/register', component: () => import('../pages/Register.vue'), meta: { hideMenu: true } },
  { name: 'Login', path: '/login', component: () => import('../pages/Login.vue'), meta: { hideMenu: true } },
  { name: 'NotFound', path: '/:pathMatch(.*)*', component: () => import('../pages/NotFound.vue') },
]
