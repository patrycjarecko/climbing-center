<template>
  <div class="flex items-center justify-center h-full">
    <div class="absolute inset-0 overflow-hidden">
      <img class="w-full" src="https://images.unsplash.com/photo-1564769662533-4f00a87b4056?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1244&q=80">
      <div class="bg-gray-600 opacity-50 absolute inset-0"></div>
    </div>
    <div class="bg-white rounded-lg shadow-xl p-6 min-w-2xl relative z-1">
      <div class="text-2xl">
        Login
      </div>
      <div class="text-sm text-gray-700 pb-8">
        Fill out the form.
      </div>

      <div class="grid grid-cols-2 gap-4 px-8">
        <it-input v-model="email" placeholder="Email" />
        <it-input v-model="password" placeholder="Password" />
      </div>

      <div class="pt-8 px-8">
        <div>
          <div class="pb-4">
            <it-checkbox v-model="remember">Remember me</it-checkbox>
          </div>

          <div >
            <it-button @click="login" :loading="loading">Login</it-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { ref } from 'vue'
import { useUserStore } from '../store'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const remember = ref(false)
const loading = ref(false)

const login = async () => {
  loading.value = true
  const error = await userStore.login(email.value, password.value)
  loading.value = false

  if (!error) {
    return router.push({ name: 'Dashboard' })
  }

}

</script>



