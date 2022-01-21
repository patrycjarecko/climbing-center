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

      <div @click="addNew" class="bg-blue-300 text-white shadow rounded px-4 py-2 text-xs cursor-pointer hover:bg-blue-400 flex items-center">
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
              <edit-icon @click="editUser(instructor)" class="text-gray-500 hover:text-blue-400 cursor-pointer mr-4" />
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

    <it-modal v-model="editMode">
      <template #header>
        <h3>Edit user</h3>
      </template>
      <template #body>
        <div class="grid grid-cols-2 gap-4">
          <it-input v-model="editedUser.firstName" label-top="First name" />
          <it-input v-model="editedUser.lastName" label-top="Last name" />
        </div>


        <div class="py-2 text-gray-800">
          Roles
        </div>
        <div v-for="role in result?.roles" :key="role.id">
          <it-checkbox type="primary" :label="role.name" v-model="editedUser.roles[role.id]" />
        </div>

        <div class="h-16"></div>
        <it-button @click="doEdit" :loading="editing" block size="big" type="primary">Edit</it-button>
      </template>
    </it-modal>

    <it-modal v-model="addMode">
      <template #header>
        <h3>Add user</h3>
      </template>
      <template #body>
        <div class="grid grid-cols-2 gap-4">
          <it-input v-model="newUser.firstName" label-top="First name" />
          <it-input v-model="newUser.lastName" label-top="Last name" />
          <it-input v-model="newUser.username" label-top="Username" />
          <it-input v-model="newUser.password" label-top="Password" />
        </div>


        <div class="py-2 text-gray-800">
          Roles
        </div>
        <div v-for="role in result?.roles" :key="role.id">
          <it-checkbox type="primary" :label="role.name" v-model="newUser.roles[role.id]" />
        </div>

        <div class="h-16"></div>
        <it-button @click="addUser" :loading="adding" block size="big" type="primary">Add</it-button>
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
import { computed, reactive, ref } from 'vue'
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

      roles { name id }
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
const { mutate: addUserMutation } = useMutation(gql`
    mutation addUser($user: InstructorInput!) {
        createInstructor(input: $user) {
          instructor {
            id
          }
        }
    }
`)
const { mutate: editUserMutation } = useMutation(gql`
    mutation editUser($id: ID!, $user: InstructorInput!) {
        updateInstructor(input: $user, id: $id) {
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




const editing = ref(false)
const editMode = ref(false)
const editedUser = reactive({
  id: null,
  roles: {},
  firstName: '',
  lastName: '',
})
const editUser = user => {
  editedUser.id = user.id
  editedUser.roles = user.role.reduce((a, b) => {
    a[b.id] = true
    return a
  }, {})
  editedUser.firstName = user.firstName
  editedUser.lastName = user.lastName
  editMode.value = true
}

const doEdit = async () => {
  editing.value = true

  await editUserMutation({
    id: editedUser.id,
    user: {
      firstName: editedUser.firstName,
      lastName: editedUser.lastName,
      roleId: Object.entries(editedUser.roles).filter(([_, enabled]) => enabled).map(([id]) => +id),
    }
  })
  await refetch()

  editing.value = false
  editMode.value = false
}

const addMode = ref(false)
const newUser = reactive({
  roles: {},
  firstName: '',
  lastName: '',
  password: '',
  username: '',
})
const addNew = () => {
  newUser.roles = {}
  newUser.firstName = ''
  newUser.lastName = ''
  newUser.password = ''
  newUser.username = ''
  addMode.value = true
}

const adding = ref(false)
const addUser = async () => {
  adding.value = true

  await addUserMutation({
    user: {
      firstName: newUser.firstName,
      lastName: newUser.lastName,
      password: newUser.password,
      username: newUser.username,
      roleId: Object.entries(newUser.roles).filter(([_, enabled]) => enabled).map(([id]) => +id),
    }
  })
  await refetch()

  adding.value = false
  addMode.value = false
}
</script>
