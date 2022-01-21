<template>
  <div class="container px-8 mx-auto pt-8">
    <div class="flex items-center pb-8">
      <div class="text-xl">
        Sections
        <div class="text-sm text-gray-600">
          List of section
        </div>
      </div>

      <div class="ml-auto"></div>

      <div @click="addNew" class="bg-blue-300 text-white shadow rounded px-4 py-2 text-xs cursor-pointer hover:bg-blue-400 flex items-center">
        <add-icon class="mr-2" />
        Create section
      </div>
    </div>
    <div class="rounded-md overflow-y-hidden shadow">
      <table class="w-full shadow">
        <tr class="text-gray-800">
          <td class="bg-gray-200 p-4">Name</td>
          <td class="bg-gray-200 p-4">Instructor</td>
          <td class="bg-gray-200 p-4">Days</td>
          <td class="bg-gray-200 p-4">Interval</td>
          <td class="bg-gray-200 p-4">People</td>
          <td class="bg-gray-200 p-4 text-right">Actions</td>
        </tr>

        <tbody class="divide-y bg-white">
          <tr v-if="!sections.length">
            <td colspan="6" class="p-4 text-center text-gray-400">No results</td>
          </tr>
          <tr v-for="section of sections">
            <td class="p-4">{{ section.sectionType.name }}</td>
            <td class="p-4">{{ section.instructor.firstName }} {{ section.instructor.lastName }}</td>
            <td class="p-4">{{ days.find(({ id }) => id === section.weekDay)?.value }}</td>
            <td class="p-4">{{ section.interval.startTime }} - {{ section.interval.endTime }}</td>
            <td class="p-4">{{ section.passSet.length }} / {{ section.sectionType.maxCount }}</td>
            <td class="p-4 text-right">
              <edit-icon @click="editSection(section)" v-if="userStore.isAdmin" class="text-gray-500 hover:text-blue-400 cursor-pointer mr-4" />
              <trash-icon @click="deleteSection(section)" v-if="canDelete" class="text-gray-500 hover:text-red-500 cursor-pointer" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <it-modal v-model="confirmDelete">
      <template #header>
        <h3>Delete section</h3>
      </template>
      <template #body>
        Section will be deleted permanently, please confirm
      </template>
      <template #actions>
        <it-button @click="confirmDelete = null">Cancel</it-button>
        <it-button type="danger" :loading="deleting" @click="deleteSection">Delete</it-button>
      </template>
    </it-modal>

    <it-modal v-model="editMode">
      <template #header>
        <h3>Edit section</h3>
      </template>
      <template #body>
        <div class="grid grid-cols-2 gap-4">
          <it-select label-top="Instructor" v-model="editedSection.instructor" :options="instructors" track-by="id">
            <template #selected-option="{ props }">
              {{ props.modelValue.firstName }} {{ props.modelValue.lastName }}
            </template>
            <template #option="{ props, option }">
              <div class="flex items-center">
                {{ option.firstName }} {{ option.lastName }}
              </div>
            </template>
          </it-select>
          <it-select label-top="Section Type" v-model="editedSection.sectionType" :options="sectionTypes" track-by="id">
            <template #selected-option="{ props }">
              {{ props.modelValue.name }}
            </template>
            <template #option="{ props, option }">
              <div class="flex items-center">
                {{ option.name }}
              </div>
            </template>
          </it-select>
          <it-select label-top="Days" v-model="editedSection.weekDay" :options="days" track-by="id">
            <template #selected-option="{ props }">
              {{ props.modelValue.value }}
            </template>
            <template #option="{ props, option }">
              <div class="flex items-center">
                {{ option.value }}
              </div>
            </template>
          </it-select>
          <it-select label-top="Intervals" v-model="editedSection.interval" :options="intervals" track-by="id">
            <template #selected-option="{ props }">
              {{ props.modelValue.startTime }} - {{ props.modelValue.endTime }}
            </template>
            <template #option="{ props, option }">
              <div class="flex items-center">
                {{ option.startTime }} - {{ option.endTime }}
              </div>
            </template>
          </it-select>
        </div>

        <div class="h-16"></div>
        <it-button @click="doEdit" :loading="editing" block size="big" type="primary">Edit</it-button>
      </template>
    </it-modal>

    <it-modal v-model="addMode">
      <template #header>
        <h3>Add section</h3>
      </template>
      <template #body>
        <div class="grid grid-cols-2 gap-4">
          <it-select label-top="Instructor" v-model="newSection.instructor" :options="instructors" track-by="id">
            <template #selected-option="{ props }">
              {{ props.modelValue.firstName }} {{ props.modelValue.lastName }}
            </template>
            <template #option="{ props, option }">
              <div class="flex items-center">
                {{ option.firstName }} {{ option.lastName }}
              </div>
            </template>
          </it-select>
          <it-select label-top="Section Type" v-model="newSection.sectionType" :options="sectionTypes" track-by="id">
            <template #selected-option="{ props }">
              {{ props.modelValue.name }}
            </template>
            <template #option="{ props, option }">
              <div class="flex items-center">
                {{ option.name }}
              </div>
            </template>
          </it-select>
          <it-select label-top="Days" v-model="newSection.weekDay" :options="days" track-by="id">
            <template #selected-option="{ props }">
              {{ props.modelValue.value }}
            </template>
            <template #option="{ props, option }">
              <div class="flex items-center">
                {{ option.value }}
              </div>
            </template>
          </it-select>
          <it-select label-top="Intervals" v-model="newSection.interval" :options="intervals" track-by="id">
            <template #selected-option="{ props }">
              {{ props.modelValue.startTime }} - {{ props.modelValue.endTime }}
            </template>
            <template #option="{ props, option }">
              <div class="flex items-center">
                {{ option.startTime }} - {{ option.endTime }}
              </div>
            </template>
          </it-select>
        </div>

        <div class="h-16"></div>
        <it-button @click="addSection" :loading="adding" block size="big" type="primary">Add</it-button>
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
      sections {
        id
        instructor {
            id
            lastName
            firstName
        }

        weekDay

        interval {
            id
            startTime
            endTime
        }

        sectionType {
            id
            name
            maxCount
        }

        passSet {
            id
        }
      }

      sectionTypes { id name }
      instructors { id firstName lastName }
      intervals { id startTime endTime }
    }
`)
const { mutate: deleteSectionMutation } = useMutation(gql`
    mutation deleteSection($id: ID!) {
        deleteSection(id: $id) {
          section {
            id
          }
        }
    }
`)
const { mutate: addSectionMutation } = useMutation(gql`
    mutation addSection($section: SectionInput!) {
        createSection(input: $section) {
          section {
            id
          }
        }
    }
`)
const { mutate: editSectionMutation } = useMutation(gql`
    mutation editSection($id: ID!, $section: SectionInput!) {
        updateSection(id: $id, input: $section) {
          section {
            id
          }
        }
    }
`)

const days = reactive([
  { id: 1, value: 'Mon, Wed' },
  { id: 2, value: 'Tue, Thu' },
])

const sections = computed(() => result.value?.sections ?? [])
const intervals = computed(() => result.value?.intervals ?? [])
const instructors = computed(() => result.value?.instructors ?? [])
const sectionTypes = computed(() => result.value?.sectionTypes ?? [])

const userStore = useUserStore()
const canDelete = computed(() => userStore.isAdmin)
const deleting = ref(false)
const sectionToDelete = ref()
const confirmDelete = ref(false)
const deleteSection = async (section = null) => {
  if (section && !(section instanceof MouseEvent)) {
    sectionToDelete.value = section
    confirmDelete.value = true
    return
  }

  if (sectionToDelete.value) {
    deleting.value = true
    await deleteSectionMutation({ id: sectionToDelete.value.id })
    await refetch()
    deleting.value = false
    sectionToDelete.value = null
    confirmDelete.value = false
  }
}

const editing = ref(false)
const editMode = ref(false)
const editedSection = reactive({
  id: null,
  interval: null,
  sectionType: null,
  instructor: null
})
const editSection = section => {
  editedSection.id = section.id
  editedSection.instructor = instructors.value.find(({ id }) => id === section.instructor.id)
  editedSection.interval = intervals.value.find(({ id }) => id === section.interval.id)
  editedSection.sectionType = sectionTypes.value.find(({ id }) => id === section.sectionType.id)
  editedSection.weekDay = days.find(({ id }) => id === section.weekDay)
  editMode.value = true
}

const doEdit = async () => {
  editing.value = true

  await editSectionMutation({
    id: editedSection.id,
    section: {
      intervalId: editedSection.interval?.id,
      instructorId: editedSection.instructor?.id,
      sectionTypeId: editedSection.sectionType?.id,
      weekDay: editedSection.weekDay?.id
    }
  })
  await refetch()

  editing.value = false
  editMode.value = false
}

const addMode = ref(false)
const newSection = reactive({
  id: null,
  instructor: null,
  interval: null,
  sectionType: null,
  weekDay: null,
})
const addNew = () => {
  newSection.instructor = null
  newSection.interval = null
  newSection.sectionType = null
  newSection.weekDay = null
  addMode.value = true
}

const adding = ref(false)
const addSection = async () => {
  adding.value = true

  await addSectionMutation({
    section: {
      intervalId: newSection.interval?.id,
      instructorId: newSection.instructor?.id,
      sectionTypeId: newSection.sectionType?.id,
      weekDay: newSection.weekDay?.id
    }
  })
  await refetch()

  adding.value = false
  addMode.value = false
}
</script>
