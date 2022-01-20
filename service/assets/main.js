import 'virtual:windi.css'
import 'virtual:windi-devtools'

import App from './App.vue'
import { createApp, h, provide } from 'vue'

import Equal from 'equal-vue'
import 'equal-vue/dist/style.css'

import router from './router'

import axios from 'axios'

import { POSITION, provideToast } from 'vue-toastification'
import 'vue-toastification/dist/index.css'

import VTooltipPlugin from 'v-tooltip'
import 'v-tooltip/dist/v-tooltip.css'

import { vfmPlugin } from 'vue-final-modal'

import { useRegisterSW } from 'virtual:pwa-register/vue'

import { DefaultApolloClient } from '@vue/apollo-composable'
import { apolloClient } from './apollo'

import { createPinia } from 'pinia'
import piniaPersist from 'pinia-plugin-persist'

// GraphQL

const app = createApp({
  setup: _ => {
    provideToast({
      timeout: 3000,
      position: POSITION.BOTTOM_RIGHT
    })

    provide(DefaultApolloClient, apolloClient)
  },
  render: _ => h(App)
})

// Pinia
const pinia = createPinia()
pinia.use(piniaPersist)
app.use(pinia)

// Equal
app.use(Equal)

// v-tooltip
app.use(VTooltipPlugin)

// Vue Final Modal
app.use(vfmPlugin)

// Devtools
if (process.env.NODE_ENV !== 'production' && '__VUE_DEVTOOLS_GLOBAL_HOOK__' in window) {
  app.config.devtools = true
  // window.__VUE_DEVTOOLS_GLOBAL_HOOK__.Vue = app
}

// axios
axios.defaults.headers.common['X-CSRFToken'] = document.querySelector('[name=csrfmiddlewaretoken]').value
axios.defaults.withCredentials = true

app.use(router)
app.mount('#app')

// Service worker
const updateServiceWorker = useRegisterSW({
  onOfflineReady () {},
})
