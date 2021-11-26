<template>
  <label class="relative mb-6 flex items-center">
    <input type="checkbox" v-model="value" />
    <div class="px-4 pb-[2px] block text-gray-500">{{ label }}</div>

    <transition name="fade">
      <span v-if="validator?.$error" class="absolute right-4 z-2">
        <span class="absolute h-0 w-0 border-4 border-transparent border-b-red-400 right-1"></span>
        <span class="bg-red-400 px-2 py-1 rounded-md text-white text-xs mt-2 block shadow">
        {{ validator?.$errors?.[0]?.$message }}
        </span>
      </span>
    </transition>
  </label>
</template>

<script setup>
import { toRefs, getCurrentInstance, watch } from 'vue'
import { useVModel } from '@vueuse/core'

const props = defineProps({
  label: String,
  value: { },
  validator: { type: Object }
})

const { validator } = toRefs(props)

const { emit } = getCurrentInstance()
const value = useVModel(props, 'value', emit)

const touch = () => validator.value?.$touch()
watch(value, () => {
  if (validator.value?.$error) {
    touch()
  }
})
</script>
