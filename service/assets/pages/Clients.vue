<template>
  <div class="container px-8 mx-auto pt-8">
    {{ clients }}
    <div class="rounded-md overflow-y-hidden shadow">
      <table class="w-full shadow">
        <tr class="text-gray-800">
          <td class="bg-gray-200 p-4">Card number</td>
          <td class="bg-gray-200 p-4">First name</td>
          <td class="bg-gray-200 p-4">Last name</td>
          <td class="bg-gray-200 p-4">Birthday date</td>
          <td class="bg-gray-200 p-4 text-right">Actions</td>
        </tr>

        <tbody class="divide-y bg-white">
          <tr>
            <td class="p-4">Card number</td>
            <td class="p-4">First name</td>
            <td class="p-4">Last name</td>
            <td class="p-4">Birthday date</td>
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
import { watchEffect } from 'vue'

const { result: clients } = useQuery(gql`
    query {
      clients {
        firstName
        lastName
        birthday
        cardNumber
      }
    }
`)

watchEffect(() => console.log(clients.value))
</script>
