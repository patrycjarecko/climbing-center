<template>
  <div class="container px-8 mx-auto pt-8">
    <div class="text-xl pb-8">
      {{ client?.firstName }} {{ client?.lastName }}
      <div class="text-sm text-gray-600">
        List of passes
      </div>
    </div>
    <div class="rounded-md overflow-y-hidden shadow">
      <table class="w-full shadow">
        <tr class="text-gray-800">
          <td class="bg-gray-200 p-4">Month</td>
          <td class="bg-gray-200 p-4">Pass type</td>
          <td class="bg-gray-200 p-4">Section</td>
          <td class="bg-gray-200 p-4">Entrances</td>
          <td class="bg-gray-200 p-4 text-right">Actions</td>
        </tr>

        <tbody class="divide-y bg-white">
        <tr v-if="!passes.length">
          <td colspan="6" class="p-4 text-center text-gray-400">No results</td>
        </tr>
        <tr v-for="pass of passes" :key="pass.id">
          <td class="p-4">{{ pass.month }}</td>
          <td class="p-4">{{ pass.passType.name }}</td>
          <td class="p-4">{{ pass.section.sectionType.name }} - {{ pass.section.instructor.firstName }} {{ pass.section.instructor.lastName }} - {{ days.find(({ id }) => id === pass.section.weekDay)?.value }} - {{ pass.section.interval.startTime }}</td>
          <td class="p-4">{{ pass.entranceSet.length }} / {{ pass.passType.maxEntryCount }}</td>
          <td class="p-4 text-right">
            <add-icon @click="addEntrance(pass)" v-if="userStore.isAdmin || userStore.isReceptionist" class="text-gray-500 hover:text-blue-500 cursor-pointer" />
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import AddIcon from '~icons/mdi/plus'
import { useMutation, useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { computed, reactive, ref } from 'vue'
import { until } from '@vueuse/core'
import { useUserStore } from '../store'
import { useRoute } from 'vue-router'

const days = reactive([
  { id: 1, value: 'Mon, Wed' },
  { id: 2, value: 'Tue, Thu' },
])

const route = useRoute()
const { result, refetch } = useQuery(gql`
    query getClient($id: String!) {
      client(id: $id) {
        cardNumber
        firstName lastName
        passSet {
            id
            month
            entranceSet { id }
            passType {
                name
                maxEntryCount
            }

            section {
                instructor {
                    firstName
                    lastName
                }
                sectionType {
                    name
                }
                interval {
                    startTime
                }
                weekDay
            }
        }
      }
    }
`, {
  id: route.params.id
})
const { mutate: createEntrance } = useMutation(gql`
    mutation createEntrance($entrance: EntranceInput!) {
        createEntrance(input: $entrance) {
          entrance {
            id
          }
        }
    }
`)

const client = computed(() => result.value?.client)
const passes = computed(() => client.value?.passSet ?? [])

const userStore = useUserStore()
const addEntrance = async pass => {
  await createEntrance({
    entrance: {
      passModelId: pass.id,
      date: new Date().toISOString().split('T')[0]
    }
  })
  await refetch()
}
</script>
