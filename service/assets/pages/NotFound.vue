<template>
  <div class="container mx-auto h-full flex flex-col justify-center py-32">
    <h1 class="text-4xl font-bold pb-2 text-yellow-400">{{ $t('messages.404') }}</h1>
    <h2 class="text-xl font-bold">{{ $t('messages.page_not_found') }}</h2>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useTitle } from '@vueuse/core'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
useTitle(t('messages.report_ticket'))
const router = useRouter()

const back = async () => {
  return router.go(-1)
}
</script>
