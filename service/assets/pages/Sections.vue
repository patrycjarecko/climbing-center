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

      <div class="bg-blue-300 text-white shadow rounded px-4 py-2 text-xs cursor-pointer hover:bg-blue-400 flex items-center">
        <add-icon class="mr-2" />
        Create section
      </div>
    </div>
    <div class="rounded-md overflow-y-hidden shadow">
      <table class="w-full shadow">
        <tr class="text-gray-800">
          <td class="bg-gray-200 p-4">Name</td>
          <td class="bg-gray-200 p-4">Instructor</td>
          <td class="bg-gray-200 p-4">Clients</td>
          <td class="bg-gray-200 p-4 text-right">Actions</td>
        </tr>

        <tbody class="divide-y bg-white">
          <tr v-if="!sections.length">
            <td colspan="6" class="p-4 text-center text-gray-400">No results</td>
          </tr>
          <tr v-for="section of sections">
            <td class="p-4">{{ section.sectionType.name }}</td>
            <td class="p-4">{{ section.instructor.firstName }} {{ section.instructor.lastName }}</td>
            <td class="p-4">{{ section.passSet.length }} / {{ section.sectionType.maxCount }}</td>
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
import AddIcon from '~icons/mdi/plus'
import EditIcon from '~icons/mdi/pencil'
import TrashIcon from '~icons/mdi/trash'
import { useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { computed } from 'vue'

const { result } = useQuery(gql`
    query {
      sections {
        id
        instructor {
            lastName
            firstName
        }

        sectionType {
            name
            maxCount
        }

        passSet {
            id
        }
      }
    }
`)

const sections = computed(() => result.value?.sections ?? [])
</script>
