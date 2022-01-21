<template>
  <div class="container px-8 mx-auto pt-8">
    <div class="flex items-center pb-8">
      <div class="text-xl">
        Intervals
        <div class="text-sm text-gray-600">
          List of interval
        </div>
      </div>

      <div class="ml-auto"></div>

      <div @click="addNew" class="bg-blue-300 text-white shadow rounded px-4 py-2 text-xs cursor-pointer hover:bg-blue-400 flex items-center">
        <add-icon class="mr-2" />
        Create interval
      </div>
    </div>
    <div class="rounded-md overflow-y-hidden shadow">
      <table class="w-full shadow">
        <tr class="text-gray-800">
          <td class="bg-gray-200 p-4">Start time</td>
          <td class="bg-gray-200 p-4">End time</td>
          <td class="bg-gray-200 p-4 text-right">Actions</td>
        </tr>

        <tbody class="divide-y bg-white">
          <tr v-if="!intervals.length">
            <td colspan="6" class="p-4 text-center text-gray-400">No results</td>
          </tr>
          <tr v-for="interval of intervals">
            <td class="p-4">{{ interval.startTime }}</td>
            <td class="p-4">{{ interval.endTime }}</td>
            <td class="p-4 text-right">
              <edit-icon @click="editInterval(interval)" v-if="userStore.isAdmin" class="text-gray-500 hover:text-blue-400 cursor-pointer mr-4" />
              <trash-icon @click="deleteInterval(interval)" v-if="userStore.isAdmin" class="text-gray-500 hover:text-red-500 cursor-pointer" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <it-modal v-model="confirmDelete">
      <template #header>
        <h3>Delete interval</h3>
      </template>
      <template #body>
        Interval will be deleted permanently, please confirm
      </template>
      <template #actions>
        <it-button @click="confirmDelete = null">Cancel</it-button>
        <it-button type="danger" :loading="deleting" @click="deleteInterval">Delete</it-button>
      </template>
    </it-modal>

    <it-modal v-model="editMode">
      <template #header>
        <h3>Edit interval</h3>
      </template>
      <template #body>
        <div class="grid grid-cols-2 gap-4">
          <it-input v-model="editedInterval.startTime" label-top="Start time" />
          <it-input v-model="editedInterval.endTime" label-top="End time" />
        </div>

        <div class="h-16"></div>
        <it-button @click="doEdit" :loading="editing" block size="big" type="primary">Edit</it-button>
      </template>
    </it-modal>

    <it-modal v-model="addMode">
      <template #header>
        <h3>Add interval</h3>
      </template>
      <template #body>
        <div class="grid grid-cols-2 gap-4">
          <it-input v-model="newInterval.startTime" label-top="Start time" />
          <it-input v-model="newInterval.endTime" label-top="End time" />
        </div>

        <div class="h-16"></div>
        <it-button @click="addInterval" :loading="adding" block size="big" type="primary">Add</it-button>
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
      intervals { id startTime endTime }
    }
`)
const { mutate: deleteIntervalMutation } = useMutation(gql`
    mutation deleteInterval($id: ID!) {
        deleteInterval(id: $id) {
          interval {
            id
          }
        }
    }
`)
const { mutate: addIntervalMutation } = useMutation(gql`
    mutation addInterval($interval: IntervalInput!) {
        createInterval(input: $interval) {
          interval {
            id
          }
        }
    }
`)
const { mutate: editIntervalMutation } = useMutation(gql`
    mutation editInterval($id: ID!, $interval: IntervalInput!) {
        updateInterval(id: $id, input: $interval) {
          interval {
            id
          }
        }
    }
`)

const intervals = computed(() => result.value?.intervals ?? [])

const userStore = useUserStore()
const canDelete = computed(() => userStore.isAdmin)
const deleting = ref(false)
const intervalToDelete = ref()
const confirmDelete = ref(false)
const deleteInterval = async (interval = null) => {
  if (interval && !(interval instanceof MouseEvent)) {
    intervalToDelete.value = interval
    confirmDelete.value = true
    return
  }

  if (intervalToDelete.value) {
    deleting.value = true
    await deleteIntervalMutation({ id: intervalToDelete.value.id })
    await refetch()
    deleting.value = false
    intervalToDelete.value = null
    confirmDelete.value = false
  }
}

const editing = ref(false)
const editMode = ref(false)
const editedInterval = reactive({
  id: null,
  startTime: null,
  endTime: null,
})
const editInterval = interval => {
  editedInterval.id = interval.id
  editedInterval.startTime = interval.startTime
  editedInterval.endTime = interval.endTime
  editMode.value = true
}

const doEdit = async () => {
  editing.value = true

  await editIntervalMutation({
    id: editedInterval.id,
    interval: {
      startTime: editedInterval.startTime,
      endTime: editedInterval.endTime,
    }
  })
  await refetch()

  editing.value = false
  editMode.value = false
}

const addMode = ref(false)
const newInterval = reactive({
  startTime: null,
  endTime: null,
})
const addNew = () => {
  newInterval.startTime = null
  newInterval.endTime = null
  addMode.value = true
}

const adding = ref(false)
const addInterval = async () => {
  adding.value = true

  await addIntervalMutation({
    interval: {
      startTime: newInterval.startTime,
      endTime: newInterval.endTime,
    }
  })
  await refetch()

  adding.value = false
  addMode.value = false
}
</script>
