export default [
  { name: 'Index', path: '/', component: () => import('../pages/Index.vue') },
  { name: 'NotFound', path: '/:pathMatch(.*)*', component: () => import('../pages/NotFound.vue') },
]
