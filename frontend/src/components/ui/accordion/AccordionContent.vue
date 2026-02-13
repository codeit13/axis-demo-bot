<script setup>
import { AccordionContent } from "reka-ui";
import { cn } from "~/lib/utils";

const props = defineProps({
  class: { type: null, required: false },
});
</script>

<template>
  <AccordionContent
    :class="
      cn(
        'overflow-hidden text-sm data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down',
        props.class
      )
    "
  >
    <div class="pb-4 pt-0">
      <slot />
    </div>
  </AccordionContent>
</template>
