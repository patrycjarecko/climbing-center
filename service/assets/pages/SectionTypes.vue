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
          <td class="bg-gray-200 p-4">Max clients</td>
          <td class="bg-gray-200 p-4 text-right">Actions</td>
        </tr>

        <tbody class="divide-y bg-white">
          <tr v-if="!sectionTypes.length">
            <td colspan="4" class="p-4 text-center text-gray-400">No results</td>
          </tr>
          <tr v-for="sectionType of sectionTypes">
            <td class="p-4">{{ sectionType.name }}</td>
            <td class="p-4">{{ sectionType.price }}</td>
            <td class="p-4">{{ sectionType.maxCount }}</td>
            <td class="p-4 text-right">
              <edit-icon @click="editSectionType(sectionType)" v-if="userStore.isAdmin" class="text-gray-500 hover:text-blue-400 cursor-pointer mr-4" />
              <trash-icon @click="deleteSectionType(sectionType)" v-if="userStore.isAdmin" class="text-gray-500 hover:text-red-500 cursor-pointer" />
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
        <it-button type="danger" :loading="deleting" @click="deleteSectionType">Delete</it-button>
      </template>
    </it-modal>

    <it-modal v-model="editMode">
      <template #header>
        <h3>Edit section</h3>
      </template>
      <template #body>
        <it-input v-model="editedSectionType.name" label-top="name" />
        <div class="grid grid-cols-2 gap-4 pt-4">
          <it-number-input v-model="editedSectionType.price" label-top="Price" :min="1" :resize-on-write="true" />
          <it-number-input v-model="editedSectionType.maxCount" label-top="count" :min="1" :resize-on-write="true" />
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
        <it-input v-model="newSectionType.name" label-top="name" />
        <div class="grid grid-cols-2 gap-4 pt-4">
          <it-number-input v-if="addMode" v-model="newSectionType.price" label-top="Price" :min="1" :resize-on-write="true" />
          <it-number-input v-if="addMode" v-model="newSectionType.maxCount" label-top="count" :min="1" :resize-on-write="true" />
        </div>

        <div class="h-16"></div>
        <it-button @click="addSectionType" :loading="adding" block size="big" type="primary">Add</it-button>
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
      sectionTypes {
        id
        name maxCount
        price
        priceOnceAWeek
      }
    }
`)
const { mutate: deleteSectionTypeMutation } = useMutation(gql`
    mutation deleteSectionType($id: ID!) {
        deleteSectiontype(id: $id) {
          sectionType {
            id
          }
        }
    }
`)
const { mutate: addSectionTypeMutation } = useMutation(gql`
    mutation addSectionType($sectionType: SectionTypeInput!) {
        createSectiontype(input: $sectionType) {
          sectionType {
            id
          }
        }
    }
`)
const { mutate: editSectionTypeMutation } = useMutation(gql`
    mutation editSectionType($id: ID!, $sectionType: SectionTypeInput!) {
        updateSectiontype(id: $id, input: $sectionType) {
          sectionType {
            id
          }
        }
    }
`)

const sectionTypes = computed(() => result.value?.sectionTypes ?? [])

const userStore = useUserStore()
const deleting = ref(false)
const sectionTypeToDelete = ref()
const confirmDelete = ref(false)
const deleteSectionType = async (sectionType = null) => {
  if (sectionType && !(sectionType instanceof MouseEvent)) {
    sectionTypeToDelete.value = sectionType
    confirmDelete.value = true
    return
  }

  if (sectionTypeToDelete.value) {
    deleting.value = true
    await deleteSectionTypeMutation({ id: sectionTypeToDelete.value.id })
    await refetch()
    deleting.value = false
    sectionTypeToDelete.value = null
    confirmDelete.value = false
  }
}

const editing = ref(false)
const editMode = ref(false)
const editedSectionType = reactive({
  id: null,
  price: 0,
  name: '',
  maxCount: 8,
})
const editSectionType = sectionType => {
  editedSectionType.id = sectionType.id
  editedSectionType.price = sectionType.price
  editedSectionType.maxCount = sectionType.maxCount
  editedSectionType.name = sectionType.name
  editMode.value = true
}

const doEdit = async () => {
  editing.value = true

  await editSectionTypeMutation({
    id: editedSectionType.id,
    sectionType: {
      price: editedSectionType.price,
      maxCount: editedSectionType.maxCount,
      name: editedSectionType.name,
    }
  })
  await refetch()

  editing.value = false
  editMode.value = false
}

const addMode = ref(false)
const newSectionType = reactive({
  id: null,
  price: 0,
  name: '',
  maxCount: 8,
})
const addNew = async () => {
  newSectionType.price = 1
  newSectionType.maxCount = 8
  newSectionType.name = ''

  await nextTick()
  addMode.value = true
}

const adding = ref(false)
const addSectionType = async () => {
  adding.value = true

  await addSectionTypeMutation({
    sectionType: {
      price: newSectionType.price,
      priceOnceAWeek: newSectionType.price,
      maxCount: newSectionType.maxCount,
      name: newSectionType.name,
    }
  })
  await refetch()

  adding.value = false
  addMode.value = false
}
</script>
