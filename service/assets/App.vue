<template>
  <div class="min-h-screen text-gray-900 grid-cols-[250px,1fr] bg-gray-100" :class="{ 'grid': !route.meta.hideMenu }">
    <div class="px-4 h-full bg-white z-1 shadow relative text-white" v-if="!route.meta.hideMenu">
      <div class="absolute inset-0 -z-1 overflow-hidden">
        <img class="w-full h-full object-cover" src="https://images.unsplash.com/photo-1599594189268-b7ce6ea1870d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80">
        <div class="bg-gray-600 opacity-50 absolute inset-0"></div>
      </div>

      <router-link :to="{ name: 'Dashboard' }" class="p-4 block flex items-center mb-4 justify-center font-bold text-xl">
        <div class="text-white">
          LOGO
        </div>
      </router-link>

      <div class="divide-y divide-white divide-opacity-20">
        <router-link :to="{ name: 'Dashboard' }" class="p-4 block flex items-center hover:text-[#fa0d]">
          <icon-stats class="mr-2" />
          Dashboard
        </router-link>
        <router-link v-if="userStore.isAdmin || userStore.isReceptionist" :to="{ name: 'Clients' }" class="p-4 block flex items-center hover:text-[#fa0d]">
          <icon-users class="mr-2" />
          Clients
        </router-link>
        <router-link v-if="userStore.isAdmin" :to="{ name: 'Users' }" class="p-4 block flex items-center hover:text-[#fa0d]">
          <icon-users class="mr-2" />
          Users
        </router-link>
        <router-link :to="{ name: 'Sections' }" class="p-4 block flex items-center hover:text-[#fa0d]">
          <icon-list class="mr-2" />
          Sections
        </router-link>
        <router-link :to="{ name: 'Passes' }" class="p-4 block flex items-center hover:text-[#fa0d]">
          <icon-list-2 class="mr-2" />
          Passes
        </router-link>
        <router-link v-if="userStore.isAdmin" :to="{ name: 'Intervals' }" class="p-4 block flex items-center hover:text-[#fa0d]">
          <icon-clock class="mr-2" />
          Intervals
        </router-link>
        <router-link v-if="userStore.isAdmin" :to="{ name: 'SectionTypes' }" class="p-4 block flex items-center hover:text-[#fa0d]">
          <icon-wunderlist class="mr-2" />
          Section Types
        </router-link>
        <router-link v-if="userStore.isAdmin" :to="{ name: 'Register' }" class="p-4 block flex items-center hover:text-[#fa0d]">
          <icon-passport class="mr-2" />
          Pass Types
        </router-link>
      </div>
    </div>

    <div class="h-full grid grid-rows-[auto,1fr]">
      <nav v-if="!route.meta.hideMenu" class="sticky shadow-md bg-white">
        <div class="container px-8 mx-auto flex items-center py-4">
          <div>{{ route.name }}</div>
          <div class="m-auto"></div>
          <router-link :to="{ name: 'Register' }">
            <it-button>
              <icon-user-add class="mr-2" />
              Add a client
            </it-button>
          </router-link>

          <div class="ml-4">
            <it-dropdown>
              <it-button>
                {{ me?.firstName }}
                {{ me?.lastName }}
              </it-button>

              <template #menu>
                <it-dropdown-menu>
<!--                  <it-dropdown-item>Hello</it-dropdown-item>-->
                  <it-dropdown-item @click="userStore.logout" icon="logout" divided>Logout</it-dropdown-item>
                </it-dropdown-menu>
              </template>
            </it-dropdown>
          </div>
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
import IconUserAdd from '~icons/mdi/user-add'
import IconUsers from '~icons/mdi/users'
import IconStats from '~icons/mdi/chart-areaspline'
import IconList from '~icons/mdi/view-list'
import IconList2 from '~icons/mdi/view-list-outline'
import IconWunderlist from '~icons/mdi/wunderlist'
import IconClock from '~icons/mdi/clock-time-eight'
import IconPassport from '~icons/mdi/passport'
import Error from './pages/Error.vue'
import { useRoute } from 'vue-router'
import { useUserStore } from './store'
import { storeToRefs } from 'pinia'
const error = '__DJANGO_ERROR__' in window
const route = useRoute()

const userStore = useUserStore()
const { me } = storeToRefs(userStore)

</script>

<style>
.router-link-exact-active {
  color: #fa0;
  font-weight: bold;
}
</style>