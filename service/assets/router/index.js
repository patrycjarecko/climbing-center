import { createRouter, createWebHistory, onBeforeRouteUpdate } from 'vue-router'
import routes from './routes'

const router = createRouter({
    history: createWebHistory(),
    routes
})


router.beforeEach(to => {
    // if (to.meta.auth && !isAuthenticated.value)  {
    //     return { name: 'Login' }
    // }
})

export default router
