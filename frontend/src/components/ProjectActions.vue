<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <!-- Left side: Create button -->
      <div>
        <button
          @click="$emit('create')"
          class="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-lg font-medium transition shadow-sm hover:shadow-md"
        >
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>New Project</span>
        </button>
      </div>

      <!-- Right side: Filters -->
      <div class="flex items-center gap-4">
        <label class="inline-flex items-center gap-2 text-sm font-medium text-gray-700 cursor-pointer">
          <input
            :checked="activeOnly"
            type="checkbox"
            class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-0"
            @change="$emit('update:activeOnly', ($event.target as HTMLInputElement).checked)"
          />
          <span>Show active only</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  activeOnly: boolean
}>()

defineEmits<{
  create: []
  'update:activeOnly': [value: boolean]
}>()
</script>
