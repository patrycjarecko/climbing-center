<template>
  <div class="min-h-screen text-gray-900 grid grid-rows-[auto,1fr]">
    <nav class="sticky">
      nav
    </nav>

    <error v-if="error" class="h-full" />
    <div v-else class="h-full">
      <router-view v-slot="{ Component, route }">
        <component :is="Component" :key="route.path" />
      </router-view>
    </div>
  </div>
</template>

<script setup>
import Error from './pages/Error.vue'
const error = '__DJANGO_ERROR__' in window
</script>