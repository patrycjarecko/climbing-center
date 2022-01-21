<template>
  <div class="container px-8 mx-auto pt-8">
    <div class="flex items-center pb-8">
      <div class="text-xl">
        Users
        <div class="text-sm text-gray-600">
          List of users
        </div>
      </div>

      <div class="ml-auto"></div>

      <div class="bg-blue-300 text-white shadow rounded px-4 py-2 text-xs cursor-pointer hover:bg-blue-400 flex items-center">
        <add-icon class="mr-2" />
        Add user
      </div>
    </div>
    <div class="rounded-md overflow-y-hidden shadow">
      <table class="w-full shadow">
        <tr class="text-gray-800">
          <td class="bg-gray-200 p-4">First name</td>
          <td class="bg-gray-200 p-4">Last name</td>
          <td class="bg-gray-200 p-4">Roles</td>
          <td class="bg-gray-200 p-4 text-right">Actions</td>
        </tr>

        <tbody class="divide-y bg-white">
        <tr v-if="!instructors.length">
          <td colspan="6" class="p-4 text-center text-gray-400">No results</td>
        </tr>
        <tr v-for="instructor of instructors" :key="instructor.id">
            <td class="p-4">{{ instructor.firstName }}</td>
            <td class="p-4">{{ instructor.lastName }}</td>
            <td class="p-4">
              <it-tag :type="tags[role.id]" filled v-for="role of instructor.role" :key="role.id" class="mr-2">
                {{ role.name }}
              </it-tag>
            </td>
            <td class="p-4 text-right">
              <edit-icon class="text-gray-500 hover:text-blue-400 cursor-pointer mr-4" />
              <trash-icon @click="deleteUser(instructor)" :class="{ '!opacity-0 !pointer-events-none': !canDelete(instructor) }" class="text-gray-500 hover:text-red-500 cursor-pointer" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <it-modal v-model="confirmDelete">
      <template #header>
        <h3>Delete user</h3>
      </template>
      <template #body>
        User will be deleted permanently, please confirm
      </template>
      <template #actions>
        <it-button @click="confirmDelete = null">Cancel</it-button>
        <it-button type="danger" :loading="deleting" @click="deleteUser">Delete</it-button>
      </template>
    </it-modal>
  </div>
</template>

<script setup>
import AddIcon from '~icons/mdi/plus'
import EditIcon from '~icons/mdi/pencil'
import TrashIcon from '~icons/mdi/trash'
import { useMutation, useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { computed, ref } from 'vue'
import { useUserStore } from '../store'

const { result, refetch } = useQuery(gql`
    query {
      users {
        id
        firstName
        lastName
        lastLogin
        role {
          id
          name
        }
      }
    }
`)
const { mutate: deleteUserMutation } = useMutation(gql`
    mutation deleteUser($id: ID!) {
        deleteInstructor(id: $id) {
          instructor {
            id
          }
        }
    }
`)

const userStore = useUserStore()

const tags = { 1: 'success', 2: 'warning', 3: 'black' }
const instructors = computed(() => result.value?.users ?? [])
const canDelete = instructor => !instructor.role.map(({ id }) => +id).includes(1) && userStore.isAdmin

const deleting = ref(false)
const userToDelete = ref()
const confirmDelete = ref(false)
const deleteUser = async (user = null) => {
  if (user && !(user instanceof MouseEvent)) {
    userToDelete.value = user
    confirmDelete.value = true
    return
  }

  if (userToDelete.value) {
    deleting.value = true
    await deleteUserMutation({ id: userToDelete.value.id })
    await refetch()
    deleting.value = false
    userToDelete.value = null
    confirmDelete.value = false
  }
}
</script>
