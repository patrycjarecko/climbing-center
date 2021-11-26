<template>
  <label class="block relative mb-6">
    <div class="px-4 pb-[2px] block text-gray-500">{{ label }}</div>
    <div ref="target" class="select-none relative">
      <div class="cursor-pointer">
        <input @click="open = true" :value="selected" :placeholder="placeholder" class="select-none pointer-events-none block px-4 py-1 text-black rounded-full w-full duration-150 outline-none shadow-md shadow-gray-200 pointer-events-none border-1" :class="$attrs.class">
      </div>
      <transition name="fade">
        <div v-if="open" class="absolute top-1/1 w-full pt-2 z-10">
          <div class="bg-white rounded border shadow-lg rounded-xl max-h-[207px] overflow-y-auto">
            <div v-for="option in options" @click.stop.prevent="select(option[optionKey])" :key="option[optionKey]" class="px-4 py-2 border-b cursor-pointer hover:(bg-yellow-200 text-black)">
              {{ option.value }}
            </div>
          </div>
        </div>
      </transition>
      <div v-if="reset && value" class="absolute right-[1px] top-1/2 transform -translate-y-1/2">
        <div @click.prevent.stop="doReset" class="h-6 w-6 bg-white rounded-full flex items-center justify-center text-xl font-thin hover:text-yellow-400 cursor-pointer">
          &times;
        </div>
      </div>
    </div>

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
import { toRefs, getCurrentInstance, watch, computed, ref } from 'vue'
import { onClickOutside, useVModel } from '@vueuse/core'

const props = defineProps({
  label: String,
  optionKey: { type: String, default: 'key' },
  options: { type: Array, required: true },
  placeholder: { type: String, default: '' },
  value: { },
  validator: { type: Object },
  reset: Boolean
})

const { validator } = toRefs(props)

const { emit } = getCurrentInstance()
const value = useVModel(props, 'value', emit)

const selected = computed(() => {
  return props?.options?.find(option => option[props.optionKey] === value.value)?.value ?? ''
})

const open = ref(false)

const touch = () => validator.value?.$touch()
watch(value, () => {
  if (validator.value?.$error) {
    touch()
  }
})

const doReset = () => {
  value.value = null
}

const select = val => {
  value.value = val
  open.value = false
}

const target = ref(null)
onClickOutside(target, () => open.value = false)
</script>

<style scoped>
::selection,
::moz-selection {
  color: currentColor;
  background: transparent;
}

.select-none,
input {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
</style>