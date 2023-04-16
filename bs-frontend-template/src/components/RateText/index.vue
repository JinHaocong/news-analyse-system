<template>
  <span
    v-if="value"
    :class="{
      'text-green-700': !positive,
      'text-red-700': positive,
      'font-bold': true,
    }"
    >{{ value }}<span v-if="per">%</span></span
  >
  <span v-else class="font-bold text-gray-700"> - </span>
</template>

<script lang="ts" setup>
import { computed } from "vue";
const props = defineProps({
  per: {
    type: Boolean,
    default: true,
  },
  value: {
    type: String,
    required: true,
  },
});
const positive = computed(() => {
  return !props.value.startsWith("-");
});
</script>