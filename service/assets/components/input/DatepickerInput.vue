<template>
  <label class="block relative mb-6">
    <div class="px-4 pb-[2px] block text-gray-500">{{ label }}</div>
    <div class="relative">
      <input ref="datepicker" @change="change" :data-date="isoDate" :placeholder="placeholder" @blur="touch" :class="{ 'ring-red-400 ring-2': validator?.$error }" readonly class="block border-1 px-4 py-1 text-black rounded-full w-full duration-150 outline-none shadow-md shadow-gray-200 focus:(text-primary shadow-lg shadow-primary)">
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

<script setup>
import { getCurrentInstance, onMounted, ref, watch, watchEffect } from 'vue'
import { Datepicker } from 'vanillajs-datepicker'
import pl from '../../../node_modules/vanillajs-datepicker/js/i18n/locales/pl.js'
import de from '../../../node_modules/vanillajs-datepicker/js/i18n/locales/de.js'
import es from '../../../node_modules/vanillajs-datepicker/js/i18n/locales/es.js'
import ru from '../../../node_modules/vanillajs-datepicker/js/i18n/locales/ru.js'
import ua from '../../../node_modules/vanillajs-datepicker/js/i18n/locales/ru.js'
import fr from '../../../node_modules/vanillajs-datepicker/js/i18n/locales/fr.js'
import it from '../../../node_modules/vanillajs-datepicker/js/i18n/locales/it.js'
import sk from '../../../node_modules/vanillajs-datepicker/js/i18n/locales/sk.js'
import nl from '../../../node_modules/vanillajs-datepicker/js/i18n/locales/nl.js'
import ro from '../../../node_modules/vanillajs-datepicker/js/i18n/locales/ro.js'
import en from '../../../node_modules/vanillajs-datepicker/js/i18n/locales/en-GB.js'
import cz from '../../../node_modules/vanillajs-datepicker/js/i18n/locales/en-GB.js'

import '../../../node_modules/vanillajs-datepicker/dist/css/datepicker.min.css'
import { useI18n } from 'vue-i18n'
import { toRefs, useVModel } from '@vueuse/core'

Object.assign(Datepicker.locales, [
  pl, en, de, es,
  ru, ua, fr, it,
  sk, cz, nl, ro
].reduce((acc, item) => {
  const [key] = Object.keys(item)
  acc[key] = item[key]
  return acc
}, {}))


const { t, locale } = useI18n()

const props = defineProps({
  label: String,
  placeholder: { type: String, default: '' },
  value: {
    type: Date,
    default: () => new Date()
  },
  allowFuture: {
    type: Boolean,
    default: true
  },
  validator: { type: Object },
  reset: Boolean
})

const { validator } = toRefs(props)

const date = props.value ?? new Date()
const isoDate = date.toISOString().split('T')[0]
const { emit } = getCurrentInstance()
const value = useVModel(props, 'value', emit)

const datepicker = ref(null)

onMounted(() => {
  const input = datepicker.value
  const picker = new Datepicker(input, {
    language: locale.value,
    format: t('format.date'),
    autohide: true,
    maxDate: props.allowFuture ? null : new Date()
  })

  watchEffect(() => {
    picker.setOptions({
      language: locale.value
    })
  })

  input.addEventListener('changeDate', ({ detail: { date } }) => {
    value.value = date || null
  })
})

const touch = () => validator.value?.$touch()
const change = () => {
  touch()
}
// watch(value, () => {
//   if (validator.value?.$error) {
//     touch()
//   }
// })

const doReset = () => {
  validator.value?.$reset()
  value.value = null
  datepicker.value.value = ''
}
</script>
