<template>
  <label class="block relative mb-6">
    <div class="px-4 pb-[2px] block text-gray-500">{{ label }}</div>
    <textarea v-if="tag === 'textarea'" :type="type" v-model="value" :placeholder="label" @blur="touch" :class="{ 'ring-red-400 ring-2': validator?.$error }" class="block px-4 py-1 text-black rounded-2xl resize-none w-full duration-150 outline-none shadow-md shadow-gray-200 border-1 focus:(text-primary shadow-lg shadow-primary)" v-bind="$attrs" />
    <input v-else :type="type" v-model="value" :placeholder="placeholder" @blur="touch" :class="{ 'ring-red-400 ring-2': validator?.$error }" class="block px-4 py-1 text-black rounded-2xl resize-none w-full duration-150 outline-none shadow-md shadow-gray-200 border-1 focus:(text-primary shadow-lg shadow-primary)" v-bind="$attrs" />
    <span v-if="value && suffix" class="absolute text-black top-9.5 left-4 pointer-events-none">
      <span class="text-transparent">{{ value }}</span>
      {{ suffix }}
    </span>

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

<script>
export default { inheritAttrs: false }
</script>
<script setup>
import { toRefs, getCurrentInstance, computed, watch } from 'vue'
import { useVModel } from '@vueuse/core'

const props = defineProps({
  label: String,
  type: { type: String, default: 'text' },
  suffix: { type: String, default: '' },
  value: { type: String, required: true },
  placeholder: { type: String, default: '' },
  validator: { type: Object },
  tag: { type: String, default: 'input' }
})

const { label, type, suffix, validator } = toRefs(props)

const { emit } = getCurrentInstance()
const value = useVModel(props, 'value', emit)

const touch = () => validator.value?.$touch()
watch(value, () => {
  if (validator.value?.$error) {
    touch()
  }
})
</script>
