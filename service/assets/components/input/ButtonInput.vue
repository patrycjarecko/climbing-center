<template>
  <div class="group cursor-pointer relative z-10 transform duration-200 hover:scale-110" v-bind="_attrs">
    <div :class="btnClass" class="px-4 py-2 bg-gray-200 rounded text-gray-700 font-bold duration-200 group-hover:bg-yellow-400 group-hover:text-white flex justify-center">
      <div :class="{ 'opacity-0 pointer-events-none': loading }">
        <slot />
      </div>
      <div v-if="loading" class="absolute inset-0 flex justify-center items-center">
        <loader />
      </div>
    </div>
    <div :class="backClass" class="bg-yellow-200 rounded text-gray-700 font-bold duration-200 transform absolute inset-0 group-hover:-rotate-3 group-hover:scale-105 -z-10"></div>
  </div>
</template>

<script>
export default { inheritAttrs: false }
</script>
<script setup>
import { computed, getCurrentInstance, ref } from 'vue'
import Loader from './Loader.vue'

const props = defineProps({
  btnClass: { type: String, default: '' },
  backClass: { type: String, default: '' }
})

const { attrs } = getCurrentInstance()

const loading = ref(false)
const _attrs = computed(() => {
  return new Proxy(attrs, {
    get (target, key) {
      if (key === 'onClick') {
        return async (...args) => {
          if (loading.value) {
            return
          }
          loading.value = true
          try {
            await target.onClick(...args)
          } catch (e) {
            console.error(e)
          } finally {
            loading.value = false
          }
        }
      }
      return target[key]
    },
    set (target, key, value) {
      target[key] = value
    }
  })
})
</script>