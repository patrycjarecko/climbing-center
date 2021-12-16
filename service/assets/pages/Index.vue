<template>
  <div class="container px-8 mx-auto flex items-center pt-8">
    <div class="grid grid-cols-3 w-full gap-4">
      <div v-for="i in 3" class="pt-12">
        <div class="shadow rounded p-4 bg-white">
          <div class="mx-1 -mt-12 shadow-md rounded p-4 bg-blue-400 text-white overflow-hidden">
            <div class="grid grid-cols-2">
              <views-icon class="h-32 w-32 -m-8 opacity-50 transform -rotate-45" />
              <div class="text-5xl text-right">
                + 274
                <div class="text-sm">new users</div>
              </div>
            </div>
          </div>
          <div class="pt-4"></div>
          <div class="text-lg text-gray-600">Website views</div>
          <div class="text-sm text-gray-400">Month to month</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ViewsIcon from '~icons/mdi/users'
</script>
