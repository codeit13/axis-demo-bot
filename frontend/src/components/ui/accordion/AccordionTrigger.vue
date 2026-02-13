<script setup>
import { AccordionHeader, AccordionTrigger } from "reka-ui";
import { cn } from "~/lib/utils";

const props = defineProps({
  class: { type: null, required: false },
});
</script>

<template>
  <AccordionHeader class="flex">
    <AccordionTrigger
      :class="
        cn(
          'flex flex-1 items-center justify-between py-4 text-sm font-medium transition-all [&[data-state=open]>svg]:rotate-180',
          props.class
        )
      "
    >
      <slot />
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="shrink-0 text-muted-foreground transition-transform duration-200"
      >
        <path d="m6 9 6 6 6-6" />
      </svg>
    </AccordionTrigger>
  </AccordionHeader>
</template>
