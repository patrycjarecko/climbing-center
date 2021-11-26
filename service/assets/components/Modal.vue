<template>
  <vue-final-modal
      v-slot="{ params, close }"
      v-bind="$attrs"
      classes="flex justify-center items-center z-110 !fixed"
      overlay-class="!fixed"
      content-class="relative flex flex-col max-h-full max-w-xl mx-4 py-4 px-6 rounded-xl bg-white shadow-xl"
      attach="body"
      :transition="{
          'enter-active-class': 'transition duration-200 ease-in-out transform',
          'enter-from-class': 'translate-y-8',
          'enter-to-class': 'translate-y-0',
          'leave-active-class': 'transition duration-200 ease-in-out transform',
          'leave-to-class': 'translate-y-8',
          'leave-from-class': 'translate-y-0'
        }"
  >
    <h1 class="text-3xl font-bold pb-6 text-gray-700">
      <slot name="title"></slot>
    </h1>

    <div class="flex-grow overflow-y-auto text-gray-600">
      <slot :params="params"></slot>
    </div>

    <div v-if="showCancel || showOk" class="flex-shrink-0 flex items-center -mb-4 -mx-6 border-t border-gray-200 font-bold">
      <div class="ml-auto"></div>
      <button v-if="showOk" class="py-2 px-4 border-l border-gray-200 hover:(bg-yellow-300 text-white)" @click="$emit('confirm', close)">
        {{ $t('messages.ok') }}
      </button>
      <button v-if="showCancel" class="py-2 px-4 border-l border-gray-200 hover:(bg-red-400 text-white) rounded-br-xl" @click="$emit('cancel', close)">
        {{ $t('messages.cancel') }}
      </button>
    </div>

    <button @click="close" class="z-1 absolute text-2xl font-thin text-white bg-red-400 rounded-full h-7 w-7 flex items-center justify-center top-0 right-0 cursor-pointer hover:bg-red-600 -translate-y-2 translate-x-2 transform">
      &times;
    </button>
  </vue-final-modal>
</template>
<script>
export default { inheritAttrs: false, emits: ['cancel', 'confirm'] }
</script>
<script setup>
const props = defineProps({
  showCancel: Boolean,
  showOk: Boolean,
})
</script>
