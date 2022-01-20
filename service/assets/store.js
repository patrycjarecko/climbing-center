import { defineStore } from 'pinia'
import { useAxios } from '@vueuse/integrations/useAxios'
import { until, useLocalStorage, useStorage } from '@vueuse/core'
import { useToast } from 'vue-toastification'
import { provideApolloClient, useQuery, useResult } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { apolloClient } from './apollo'
import router from './router'

const toast = useToast()
export const useUserStore = defineStore('counter', {
  state: () => ({
    token:  null,
    me:  null
  }),
  getters: {
    isAuthenticated: state => state.me !== null
  },
  actions: {
    async login (username, password) {
      const { data, error, isFinished } = useAxios('/api/login', {
        method: 'POST',
        data: { username, password }
      })

      await until(isFinished).toBe(true)
      if (error.value) {
        toast.error('Bledny email i haslo')
        return error.value
      }

      provideApolloClient(apolloClient)
      const { token } = data.value
      const { result } = useQuery(gql`
          query me($token: String!) {
              instructor(token: $token) {
                  role { id name }
                  firstName lastName
                  username
              }
          }
      `, { token })

      const me = useResult(result)
      await until(me).toBeTruthy()

      this.me = me.value
      this.token = token
    },
    logout () {
      this.me = null
      this.token = null
      return router.push({ name: 'Login' })
    }
  },
  persist: {
    enabled: true,
    strategies: [{ key: 'user', storage: localStorage }]
  }
})
