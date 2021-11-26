<template>
  <div>
    {{ status }}
    {{ message }}
  </div>
</template>

<script setup>
const { status, message } = window.__DJANGO_ERROR__
</script>
