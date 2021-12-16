<template>
  <div class="min-h-screen text-gray-900 grid grid-rows-[auto,1fr]">
    <nav class="sticky flex">
      <div>a</div>
      <div class="m-auto"></div>
      <router-link :to="{ name: 'Register' }" class="p-4 block">
        Register
      </router-link>
    </nav>

    <error v-if="error" class="h-full" />
    <div v-else class="h-full">
      <router-view v-slot="{ Component, route }">
        <template v-if="Component">
          <transition mode="out-in">
            <keep-alive>
              <suspense>
                <component :is="Component" :key="route.path"></component>
                <template #fallback>
                  <div>
                    Loading...
                  </div>
                </template>
              </suspense>
            </keep-alive>
          </transition>
        </template>
      </router-view>

    </div>
  </div>
</template>

<script setup>
import Error from './pages/Error.vue'
const error = '__DJANGO_ERROR__' in window
</script>