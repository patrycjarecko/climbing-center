<template>
  <div class="container px-8 mx-auto pt-8">
    <div class="flex items-center pb-8">
      <div class="text-xl">
        Passes
        <div class="text-sm text-gray-600">
          List of passes
        </div>
      </div>

      <div class="ml-auto"></div>

      <div @click="addNew" class="bg-blue-300 text-white shadow rounded px-4 py-2 text-xs cursor-pointer hover:bg-blue-400 flex items-center">
        <add-icon class="mr-2" />
        Create pass
      </div>
    </div>
    <div class="rounded-md overflow-y-hidden shadow">
      <table class="w-full shadow">
        <tr class="text-gray-800">
          <td class="bg-gray-200 p-4">Client</td>
          <td class="bg-gray-200 p-4">Month</td>
          <td class="bg-gray-200 p-4">Pass type</td>
          <td class="bg-gray-200 p-4">Section</td>
          <td class="bg-gray-200 p-4 text-right">Actions</td>
        </tr>

        <tbody class="divide-y bg-white">
          <tr v-if="!passes.length">
            <td colspan="5" class="p-4 text-center text-gray-400">No results</td>
          </tr>
          <tr v-for="pass of passes">
            <td class="p-4">{{ pass.client.firstName }} {{ pass.client.lastName }}</td>
            <td class="p-4">{{ pass.month }}</td>
            <td class="p-4">{{ pass.passType.name }}</td>
            <td class="p-4">{{ pass.section.sectionType.name }} - {{ pass.section.instructor.firstName }} {{ pass.section.instructor.lastName }} - {{ days.find(({ id }) => id === pass.section.weekDay)?.value }} - {{ pass.section.interval.startTime }}</td>
            <td class="p-4 text-right">
              <trash-icon @click="deletePass(pass)" v-if="userStore.isAdmin" class="text-gray-500 hover:text-red-500 cursor-pointer" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <it-modal v-model="confirmDelete">
      <template #header>
        <h3>Delete pass</h3>
      </template>
      <template #body>
        Pass will be deleted permanently, please confirm
      </template>
      <template #actions>
        <it-button @click="confirmDelete = null">Cancel</it-button>
        <it-button type="danger" :loading="deleting" @click="deletePass">Delete</it-button>
      </template>
    </it-modal>

    <it-modal v-model="addMode">
      <template #header>
        <h3>Add pass</h3>
      </template>
      <template #body>
        <div class="grid grid-cols-2 gap-4">
          <it-select label-top="Client" v-model="newPass.client" :options="clients" track-by="cardNumber">
            <template #selected-option="{ props }">
              {{ props.modelValue.firstName }} {{ props.modelValue.lastName }}
            </template>
            <template #option="{ props, option }">
              <div class="flex items-center">
                {{ option.firstName }} {{ option.lastName }}
              </div>
            </template>
          </it-select>
          <it-select label-top="Pass Type" v-model="newPass.passType" :options="passTypes" track-by="id">
            <template #selected-option="{ props }">
              {{ props.modelValue.name }}
            </template>
            <template #option="{ props, option }">
              <div class="flex items-center">
                {{ option.name }}
              </div>
            </template>
          </it-select>
        </div>

        <div class="pt-4 flex">
          <it-select label-top="Section" v-model="newPass.section" :options="sections" track-by="id" class="w-full">
            <template #selected-option="{ props }">
              {{ props.modelValue.sectionType.name }} - {{ props.modelValue.instructor.firstName }} {{ props.modelValue.instructor.lastName }} - {{ days.find(({ id }) => id === props.modelValue.weekDay)?.value }} - {{ props.modelValue.interval.startTime }}
            </template>
            <template #option="{ props, option }">
              <div class="flex items-center">
                {{ option.sectionType.name }} - {{ option.instructor.firstName }} {{ option.instructor.lastName }} - {{ days.find(({ id }) => id === option.weekDay)?.value }} - {{ option.interval.startTime }}
              </div>
            </template>
          </it-select>
        </div>

        <div class="h-16"></div>
        <it-button @click="addPass" :loading="adding" block size="big" type="primary">Add</it-button>
      </template>
    </it-modal>
  </div>
</template>

<script setup>
import AddIcon from '~icons/mdi/plus'
import TrashIcon from '~icons/mdi/trash'
import { useMutation, useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { computed, reactive, ref } from 'vue'
import { useUserStore } from '../store'

const { result, refetch } = useQuery(gql`
    query {
      passes {
        id
        section {
            sectionType {
                name
            }

            interval {
                startTime
            }

            instructor {
                firstName
                lastName
            }

            weekDay
        }

        client {
            firstName
            lastName
        }
        month
        passType {
            name
        }
      }

      clients {
        firstName
        lastName
        cardNumber
      }

      passTypes {
        id
        name
      }

      sections {
          id
          sectionType {
              name
          }

          interval {
              startTime
          }

          instructor {
              firstName
              lastName
          }

          weekDay
      }
    }
`)
const { mutate: deletePassMutation } = useMutation(gql`
    mutation deletePass($id: ID!) {
        deletePass(id: $id) {
          passModel {
            id
          }
        }
    }
`)
const { mutate: addPassMutation } = useMutation(gql`
    mutation addPass($pass: PassInput!) {
        createPass(input: $pass) {
          passModel {
            id
          }
        }
    }
`)

const days = reactive([
  { id: 1, value: 'Mon, Wed' },
  { id: 2, value: 'Tue, Thu' },
])

const passes = computed(() => result.value?.passes ?? [])
const clients = computed(() => result.value?.clients ?? [])
const passTypes = computed(() => result.value?.passTypes ?? [])
const sections = computed(() => result.value?.sections ?? [])

const userStore = useUserStore()
const deleting = ref(false)
const passToDelete = ref()
const confirmDelete = ref(false)
const deletePass = async (pass = null) => {
  if (pass && !(pass instanceof MouseEvent)) {
    passToDelete.value = pass
    confirmDelete.value = true
    return
  }

  if (passToDelete.value) {
    deleting.value = true
    await deletePassMutation({ id: passToDelete.value.id })
    await refetch()
    deleting.value = false
    passToDelete.value = null
    confirmDelete.value = false
  }
}

const addMode = ref(false)
const newPass = reactive({
  id: null,
  client: null,
  passType: null,
  section: null,
})
const addNew = () => {
  newPass.client = null
  newPass.passType = null
  newPass.section = null
  addMode.value = true
}

const adding = ref(false)
const addPass = async () => {
  adding.value = true

  await addPassMutation({
    pass: {
      clientId: newPass.client?.cardNumber,
      month: new Date().toISOString().split('T')[0],
      passTypeId: newPass.passType?.id,
      sectionId: newPass.section?.id
    }
  })
  await refetch()

  adding.value = false
  addMode.value = false
}
</script>
