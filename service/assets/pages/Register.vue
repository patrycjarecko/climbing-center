<template>
  <div class="flex items-center justify-center h-full">
    <div class="absolute inset-0 overflow-hidden">
      <img class="w-full" src="https://images.unsplash.com/photo-1571649123442-dc0e1965e037?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80">
      <div class="bg-gray-600 opacity-50 absolute inset-0"></div>
    </div>
    <div class="bg-white rounded-lg shadow-xl p-6 min-w-2xl relative z-1 overflow-hidden">
      <it-progressbar v-if="loading" infinite :height="4" class="absolute top-0 left-0" />
      <div class="flex pb-8">
        <div class="w-8 flex items-center text-gray-400">
          <icon-user class="w-6 h-6" />
        </div>
        <div>
          <div class="text-2xl">
            Register client
          </div>
          <div class="text-sm text-gray-700">
            Fill out the form.
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4 px-8">
        <it-input v-model="firstname" placeholder="First name" />
        <it-input v-model="lastname" placeholder="Last name" />
        <it-input v-model="email" placeholder="Email" />
        <it-input v-model="date" placeholder="Birthday date" />
      </div>

      <div class="pt-8 px-8">
        <div>
          <div class="pb-4">
            <it-checkbox>I accept the Terms of Services</it-checkbox>
          </div>

          <div >
            <it-button @click="register">Register</it-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import IconUser from '~icons/mdi/user'
import { reactive, ref, watchEffect } from 'vue'
import gql from 'graphql-tag'
import { useMutation } from '@vue/apollo-composable'
import { useRouter } from 'vue-router'
import { Message } from 'equal-vue'

const router = useRouter()

const firstname = ref('')
const lastname = ref('')
const email = ref('')
const date = ref('')

const { mutate, loading, onDone, onError } = useMutation(gql`mutation createClient($firstname: String!, $lastname: String!, $email: String!, $date: Date!) {
    createClient(input: { firstName: $firstname, lastName: $lastname, email: $email, birthday: $date }) {
      client {
        cardNumber
      }
    }
  }`, {
  variables: reactive({
    firstname,
    lastname,
    email,
    date
  })
})

onDone(client => {
  router.push({ name: 'Clients' })
})

onError(err => {
  Message.danger({
    text: 'An error occured, check the console.'
  })

  console.error(err)
})

const register = async () => {
  mutate()
}
</script>



