<script setup>
import { cn } from '~/lib/utils';

const props = defineProps({
  align: { type: String, required: false, default: 'inline-start' },
  class: { type: null, required: false },
});
</script>

<template>
  <div
    :class="
      cn(
        'flex items-center justify-center border-input bg-muted px-3 text-muted-foreground',
        props.align === 'inline-start' && 'border-r',
        props.align === 'inline-end' && 'border-l',
        props.class,
      )
    "
  >
    <slot />
  </div>
</template>
