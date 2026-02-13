<script setup>
import { AccordionItem } from "reka-ui";
import { cn } from "~/lib/utils";

const props = defineProps({
  value: { type: String, required: true },
  disabled: { type: Boolean, required: false },
  class: { type: null, required: false },
});
</script>

<template>
  <AccordionItem
    v-bind="props"
    :class="cn('border-b', props.class)"
  >
    <slot />
  </AccordionItem>
</template>
