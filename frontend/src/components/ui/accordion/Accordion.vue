<script setup>
import { AccordionRoot, useForwardPropsEmits } from "reka-ui";

const props = defineProps({
  type: { type: String, required: false, default: "single" },
  defaultValue: { type: [String, Array], required: false },
  modelValue: { type: [String, Array], required: false },
  collapsible: { type: Boolean, required: false, default: true },
  disabled: { type: Boolean, required: false },
  dir: { type: String, required: false },
  orientation: { type: String, required: false },
  class: { type: null, required: false },
});

const emits = defineEmits(["update:modelValue"]);
const forwarded = useForwardPropsEmits(props, emits);
</script>

<template>
  <AccordionRoot v-bind="forwarded">
    <slot />
  </AccordionRoot>
</template>
