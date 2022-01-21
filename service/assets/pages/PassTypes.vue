<template>
  <div class="container px-8 mx-auto pt-8">
    <div class="flex items-center pb-8">
      <div class="text-xl">
        Section types
        <div class="text-sm text-gray-600">
          List of section types
        </div>
      </div>

      <div class="ml-auto"></div>

      <div @click="addNew" class="bg-blue-300 text-white shadow rounded px-4 py-2 text-xs cursor-pointer hover:bg-blue-400 flex items-center">
        <add-icon class="mr-2" />
        Create section type
      </div>
    </div>
    <div class="rounded-md overflow-y-hidden shadow">
      <table class="w-full shadow">
        <tr class="text-gray-800">
          <td class="bg-gray-200 p-4">Name</td>
          <td class="bg-gray-200 p-4">Price</td>
          <td class="bg-gray-200 p-4">Max entries</td>
          <td class="bg-gray-200 p-4">Duration</td>
          <td class="bg-gray-200 p-4 text-right">Actions</td>
        </tr>

        <tbody class="divide-y bg-white">
          <tr v-if="!passTypes.length">
            <td colspan="4" class="p-4 text-center text-gray-400">No results</td>
          </tr>
          <tr v-for="passType of passTypes">
            <td class="p-4">{{ passType.name }}</td>
            <td class="p-4">{{ passType.price }}</td>
            <td class="p-4">{{ passType.maxEntryCount }}</td>
            <td class="p-4">{{ passType.expirationDate }}</td>
            <td class="p-4 text-right">
              <edit-icon @click="editPassType(passType)" v-if="userStore.isAdmin" class="text-gray-500 hover:text-blue-400 cursor-pointer mr-4" />
              <trash-icon @click="deletePassType(passType)" v-if="userStore.isAdmin" class="text-gray-500 hover:text-red-500 cursor-pointer" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <it-modal v-model="confirmDelete">
      <template #header>
        <h3>Delete section type</h3>
      </template>
      <template #body>
        Section type will be deleted permanently, please confirm
      </template>
      <template #actions>
        <it-button @click="confirmDelete = null">Cancel</it-button>
        <it-button type="danger" :loading="deleting" @click="deletePassType">Delete</it-button>
      </template>
    </it-modal>

    <it-modal v-model="editMode">
      <template #header>
        <h3>Edit section</h3>
      </template>
      <template #body>
        <it-input v-model="editedPassType.name" label-top="name" />
        <div class="grid grid-cols-2 gap-4 pt-4">
          <it-number-input v-model="editedPassType.price" label-top="Price" :min="1" :resize-on-write="true" />
          <it-number-input v-model="editedPassType.maxEntryCount" label-top="Max entries" :min="1" :resize-on-write="true" />
          <it-number-input v-model="editedPassType.duration" label-top="Duration (months)" :min="1" :resize-on-write="true" />
        </div>

        <div class="h-16"></div>
        <it-button @click="doEdit" :loading="editing" block size="big" type="primary">Edit</it-button>
      </template>
    </it-modal>

    <it-modal v-model="addMode">
      <template #header>
        <h3>Add section type</h3>
      </template>
      <template #body>
        <it-input v-model="newPassType.name" label-top="name" />
        <div class="grid grid-cols-2 gap-4 pt-4">
          <it-number-input v-if="addMode" v-model="newPassType.price" label-top="Price" :min="1" :resize-on-write="true" />
          <it-number-input v-if="addMode" v-model="newPassType.maxEntryCount" label-top="Max entries" :min="1" :resize-on-write="true" />
          <it-number-input v-if="addMode" v-model="newPassType.duration" label-top="Duration (months)" :min="1" :resize-on-write="true" />
        </div>

        <div class="h-16"></div>
        <it-button @click="addPassType" :loading="adding" block size="big" type="primary">Add</it-button>
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
import { computed, nextTick, reactive, ref } from 'vue'
import { useUserStore } from '../store'

const { result, refetch } = useQuery(gql`
    query {
      passTypes {
        id
        name
        price
        expirationDate
        maxEntryCount
      }
    }
`)
const { mutate: deletePassTypeMutation } = useMutation(gql`
    mutation deletePassType($id: ID!) {
        deletePasstype(id: $id) {
          passType {
            id
          }
        }
    }
`)
const { mutate: addPassTypeMutation } = useMutation(gql`
    mutation addPassType($passType: PassTypeInput!) {
        createPasstype(input: $passType) {
          passType {
            id
          }
        }
    }
`)
const { mutate: editPassTypeMutation } = useMutation(gql`
    mutation editPassType($id: ID!, $passType: PassTypeInput!) {
        updatePasstype(id: $id, input: $passType) {
          passType {
            id
          }
        }
    }
`)

const passTypes = computed(() => result.value?.passTypes ?? [])

const userStore = useUserStore()
const deleting = ref(false)
const passTypeToDelete = ref()
const confirmDelete = ref(false)
const deletePassType = async (passType = null) => {
  if (passType && !(passType instanceof MouseEvent)) {
    passTypeToDelete.value = passType
    confirmDelete.value = true
    return
  }

  if (passTypeToDelete.value) {
    deleting.value = true
    await deletePassTypeMutation({ id: passTypeToDelete.value.id })
    await refetch()
    deleting.value = false
    passTypeToDelete.value = null
    confirmDelete.value = false
  }
}

const editing = ref(false)
const editMode = ref(false)
const editedPassType = reactive({
  id: null,
  price: 0,
  name: '',
  maxEntryCount: 8,
})
const editPassType = passType => {
  editedPassType.id = passType.id
  editedPassType.price = passType.price
  editedPassType.duration = 1
  editedPassType.maxEntryCount = passType.maxEntryCount
  editedPassType.name = passType.name
  editMode.value = true
}

const doEdit = async () => {
  editing.value = true

  await editPassTypeMutation({
    id: editedPassType.id,
    passType: {
      price: editedPassType.price,
      maxEntryCount: editedPassType.maxEntryCount,
      expirationDate: editedPassType.duration,
      name: editedPassType.name,
    }
  })
  await refetch()

  editing.value = false
  editMode.value = false
}

const addMode = ref(false)
const newPassType = reactive({
  id: null,
  price: 0,
  name: '',
  maxEntryCount: 8,
})
const addNew = async () => {
  newPassType.price = 1
  newPassType.duration = 1
  newPassType.maxEntryCount = 8
  newPassType.name = ''

  await nextTick()
  addMode.value = true
}

const adding = ref(false)
const addPassType = async () => {
  adding.value = true

  await addPassTypeMutation({
    passType: {
      price: newPassType.price,
      maxEntryCount: newPassType.maxEntryCount,
      expirationDate: newPassType.duration,
      name: newPassType.name,
    }
  })
  await refetch()

  adding.value = false
  addMode.value = false
}
</script>
