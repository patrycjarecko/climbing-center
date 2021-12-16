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
              <edit-icon class="text-gray-500 hover:text-blue-400 cursor-pointer mr-4" />
              <trash-icon class="text-gray-500 hover:text-red-500 cursor-pointer" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import EditIcon from '~icons/mdi/pencil'
import TrashIcon from '~icons/mdi/trash'
import { useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { computed } from 'vue'

const { result } = useQuery(gql`
    query {
      clients {
        firstName
        lastName
        birthday
        cardNumber
      }
    }
`)

const clients = computed(() => result.value?.instructors ?? [])
</script>
