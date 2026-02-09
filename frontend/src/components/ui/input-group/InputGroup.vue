<script setup>
import { cn } from '~/lib/utils';

const props = defineProps({
  class: { type: null, required: false },
});
</script>

<template>
  <div
    :class="
      cn(
        'flex items-center gap-0 overflow-hidden rounded-md border border-input bg-background text-sm ring-offset-background focus-within:ring-1 focus-within:ring-ring',
        props.class,
      )
    "
  >
    <slot />
  </div>
</template>
