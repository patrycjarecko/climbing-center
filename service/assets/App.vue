<template>
  <div class="min-h-screen text-gray-900 grid-cols-[250px,1fr]" :class="{ 'grid': !route.meta.hideMenu }">
    <div class="px-4 h-full bg-white z-1 shadow relative" v-if="!route.meta.hideMenu">
      <div class="absolute inset-0 -z-1 overflow-hidden">
        <img class="w-full h-full object-cover" src="https://images.unsplash.com/photo-1599594189268-b7ce6ea1870d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80">
        <div class="bg-gray-600 opacity-50 absolute inset-0"></div>
      </div>
    </div>

    <div class="h-full grid grid-rows-[auto,1fr]">
      <nav v-if="!route.meta.hideMenu" class="sticky shadow-md">
        <div class="container px-8 mx-auto flex items-center">
          <div>a</div>
          <div class="m-auto"></div>
          <router-link :to="{ name: 'Register' }" class="p-4 block">
            Register
          </router-link>
        </div>
      </nav>
      <div v-else></div>

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
  </div>
</template>

<script setup>
import Error from './pages/Error.vue'
import { useRoute } from 'vue-router'
const error = '__DJANGO_ERROR__' in window
const route = useRoute()
</script>