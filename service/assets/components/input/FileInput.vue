<template>
  <label class="grid grid-rows-[auto,1fr] relative mb-6">
    <div class="px-4 pb-[2px] block text-gray-500">{{ label }}</div>
    <div :class="{ 'ring-red-400 ring-2': validator?.$error }" class="block p-2 text-black rounded-2xl w-full duration-150 outline-none shadow-md shadow-gray-200 border-1 h-full flex items-center justify-center font-bold text-xs text-gray-400 relative h-full">
      <div v-if="!value.length">
        {{ $t('messages.upload_file') }}
      </div>
      <div v-else class="relative h-full">
        <template v-if="!multiple && isImage(value?.[0].name ?? '')">
          <img :src="src" alt="" class="rounded-xl block h-full">
          <div @click.stop.prevent="remove(0)" class="z-1 absolute text-2xl font-thin text-white bg-red-400 rounded-full h-7 w-7 flex items-center justify-center top-0 right-0 cursor-pointer hover:bg-red-600 -translate-y-[.25rem] translate-x-[.25rem] transform">
            &times;
          </div>
        </template>
        <template v-else>
          <div v-for="(file, i) in value" class="text-xs font-semibold flex pb-1">
            <component :is="useFileIcon(file.name.toLowerCase())" />
            <div class="mx-1 w-36">
              <div class="truncate">
                {{ file.name }}
              </div>
            </div>
            <div @click="remove(i)" class="z-1 realtive ml-auto text-white bg-red-400 rounded-full flex items-center justify-center h-4 w-4 cursor-pointer hover:bg-red-600 flex-shrink-0">
              &times;
            </div>
          </div>
        </template>


      </div>

      <input type="file" ref="file" @blur="touch" @change="change" :multiple="multiple" :accept="allowedExtensions.join(',')" class="absolute opacity-0 inset-0" />
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

<script setup>
import { toRefs, getCurrentInstance, computed, watch, ref } from 'vue'
import { useVModel } from '@vueuse/core'
import { useFileIcon } from '../utils'

const props = defineProps({
  label: String,
  value: { type: Array, required: true },
  multiple: { type: Boolean, default: false },
  allowedExtensions: {
    type: Array,
    default: () => [
      '.txt', '.doc', '.docx', '.odt', '.pdf',
      '.xlsx', '.xlsm', '.csv',
      '.mp3', '.3gp', '.wav',
      '.avi', '.mp4', '.mpg',
      '.jpg', '.png', '.jpeg', '.webp'
    ]
  },
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

const file = ref(null)
const src = computed(() => {
  if (value.value.length === 0) {
    return null
  }

  return URL.createObjectURL(value.value[0])
})
const change = () => {
  if (!props.multiple) {
    value.value.length = 0
  }

  for (const blob of file.value.files) {
    if (props.allowedExtensions.some(ext => blob.name.toLowerCase().endsWith(ext))) {
      value.value.push(blob)
    }
  }
}

const remove = (i) => {
  value.value.splice(i, 1)
}

const isImage = name => {
  return ['.jpg', '.png', '.jpeg', '.webp'].some(ext => name.toLowerCase().endsWith(ext))
}
</script>
