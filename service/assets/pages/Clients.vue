<template>
  <div class="container px-8 mx-auto pt-8">
    <div class="text-xl pb-8">
      Clients
      <div class="text-sm text-gray-600">
        List of clients
      </div>
    </div>
    <div class="rounded-md overflow-y-hidden shadow">
      <table class="w-full shadow">
        <tr class="text-gray-800">
          <td class="bg-gray-200 p-4">Card number</td>
          <td class="bg-gray-200 p-4">First name</td>
          <td class="bg-gray-200 p-4">First name</td>
          <td class="bg-gray-200 p-4">Email</td>
          <td class="bg-gray-200 p-4">Birthday date</td>
          <td class="bg-gray-200 p-4 text-right">Actions</td>
        </tr>

        <tbody class="divide-y bg-white">
        <tr v-if="!clients.length">
          <td colspan="6" class="p-4 text-center text-gray-400">No results</td>
        </tr>
        <tr v-for="client of clients">
          <td class="p-4">{{ client.cardNumber }}</td>
          <td class="p-4">{{ client.firstName }}</td>
          <td class="p-4">{{ client.lastName }}</td>
          <td class="p-4">{{ client.email }}</td>
          <td class="p-4">{{ client.birthday }}</td>
          <td class="p-4 text-right">
            <edit-icon @click="editClient(client)" v-if="userStore.isAdmin || userStore.isReceptionist" class="text-gray-500 hover:text-blue-400 cursor-pointer mr-4" />
            <trash-icon v-if="userStore.isAdmin" @click="deleteClient(client)" class="text-gray-500 hover:text-red-500 cursor-pointer" />
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <it-modal v-model="confirmDelete">
      <template #header>
        <h3>Delete client</h3>
      </template>
      <template #body>
        Client will be deleted permanently, please confirm
      </template>
      <template #actions>
        <it-button @click="confirmDelete = null">Cancel</it-button>
        <it-button type="danger" :loading="deleting" @click="deleteClient">Delete</it-button>
      </template>
    </it-modal>

    <it-modal v-model="editMode">
      <template #header>
        <h3>Edit client</h3>
      </template>
      <template #body>
        <div class="grid grid-cols-2 gap-4">
          <it-input v-model="editedClient.firstName" />
          <it-input v-model="editedClient.lastName" />
          <it-input v-model="editedClient.email" />
        </div>

        <div class="h-16"></div>
        <it-button @click="doEdit" :loading="editing" block size="big" type="primary">Edit</it-button>
      </template>
    </it-modal>
  </div>
</template>

<script setup>
import EditIcon from '~icons/mdi/pencil'
import TrashIcon from '~icons/mdi/trash'
import { useMutation, useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { computed, reactive, ref } from 'vue'
import { until } from '@vueuse/core'
import { useUserStore } from '../store'

const { result, refetch } = useQuery(gql`
    query {
      clients {
        cardNumber
        firstName
        lastName
        birthday
        cardNumber
        email
      }
    }
`)
const { mutate: deleteClientMutation } = useMutation(gql`
    mutation deleteClient($cardNumber: String!) {
        deleteClient(id: $cardNumber) {
            client {
                cardNumber
            }
        }
    }
`)
const { mutate: editClientMutation } = useMutation(gql`
    mutation editClient($cardNumber: String!, $client: ClientInput!) {
        updateClient(id: $cardNumber, input: $client) {
            client {
                cardNumber
            }
        }
    }
`)

const clients = computed(() => result.value?.clients ?? [])

const userStore = useUserStore()
const deleting = ref(false)
const clientToDelete = ref()
const confirmDelete = ref(false)
const deleteClient = async (client = null) => {
  if (client && !(client instanceof MouseEvent)) {
    clientToDelete.value = client
    confirmDelete.value = true
    return
  }

  if (clientToDelete.value) {
    deleting.value = true
    await deleteClientMutation({ cardNumber: clientToDelete.value.cardNumber })
    await refetch()
    deleting.value = false
    clientToDelete.value = null
    confirmDelete.value = false
  }
}

const editing = ref(false)
const editMode = ref(false)
const editedClient = reactive({
  id: null,
  interval: null,
  clientType: null,
  instructor: null
})
const editClient = client => {
  editedClient.id = client.cardNumber
  editedClient.firstName = client.firstName
  editedClient.lastName = client.lastName
  editedClient.email = client.email
  editMode.value = true
}

const doEdit = async () => {
  editing.value = true

  await editClientMutation({
    cardNumber: editedClient.id,
    client: {
      firstName: editedClient.firstName,
      lastName: editedClient.lastName,
      email: editedClient.email
    }
  })
  await refetch()

  editing.value = false
  editMode.value = false
}
</script>
