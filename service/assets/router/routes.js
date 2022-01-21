export default [
  { name: 'Dashboard', path: '/', component: () => import('../pages/Index.vue') },
  { name: 'Clients', path: '/clients', component: () => import('../pages/Clients.vue') },
  { name: 'Users', path: '/users', component: () => import('../pages/Users.vue') },
  { name: 'Sections', path: '/sections', component: () => import('../pages/Sections.vue') },
  { name: 'Passes', path: '/passes', component: () => import('../pages/Passes.vue') },
  { name: 'Intervals', path: '/intervals', component: () => import('../pages/Intervals.vue') },
  { name: 'SectionTypes', path: '/section-types', component: () => import('../pages/SectionTypes.vue') },
  { name: 'Register', path: '/register', component: () => import('../pages/Register.vue'), meta: { hideMenu: true } },
  { name: 'Login', path: '/login', component: () => import('../pages/Login.vue'), meta: { hideMenu: true } },
  { name: 'NotFound', path: '/:pathMatch(.*)*', component: () => import('../pages/NotFound.vue') },
]
