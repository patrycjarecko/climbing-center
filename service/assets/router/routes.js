export default [
  { name: 'Index', path: '/', component: () => import('../pages/Index.vue') },
  { name: 'Register', path: '/register', component: () => import('../pages/Register.vue'), meta: { hideMenu: true } },
  { name: 'NotFound', path: '/:pathMatch(.*)*', component: () => import('../pages/NotFound.vue') },
]
