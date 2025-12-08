<template>
  <div class="flex flex-col bg-white rounded-lg border border-gray-200 p-4">
    <!-- Column Header -->
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
      <span class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-gray-200 text-sm font-medium text-gray-700">
        {{ tasks.length }}
      </span>
    </div>

    <!-- Tasks List -->
    <div class="flex flex-col gap-3">
      <div
        v-for="task in tasks"
        :key="task.id"
        @click="$emit('task-click', task)"
        class="p-4 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition cursor-pointer"
        :class="bgColor"
      >
        <div class="flex items-start justify-between mb-2">
          <h4 class="font-medium text-gray-900">{{ task.title }}</h4>
          <span
            class="px-2 py-1 text-xs font-medium rounded"
            :class="getPriorityClass(task.priority || 'medium')"
          >
            {{ task.priority }}
          </span>
        </div>
        
        <p class="text-sm text-gray-600 mb-3 line-clamp-2">{{ task.description }}</p>
        
        <div class="flex items-center justify-between text-xs text-gray-500">
          <div v-if="task.assigned_to" class="flex items-center gap-2">
            <div class="w-6 h-6 rounded-full bg-blue-600 flex items-center justify-center text-white font-medium">
              {{ task.assigned_to.charAt(0) }}
            </div>
            <span>{{ task.assigned_to }}</span>
          </div>
          <span v-else class="text-gray-400">Unassigned</span>
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-if="tasks.length === 0"
        class="flex flex-col items-center justify-center py-8 text-center"
      >
        <svg class="w-12 h-12 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="text-sm text-gray-500">No tasks</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Task } from '@/services/api'

defineProps<{
  title: string
  tasks: Task[]
  status: string
  bgColor: string
}>()

defineEmits<{
  'task-click': [task: Task]
}>()

const getPriorityClass = (priority: string) => {
  switch (priority) {
    case 'high':
      return 'bg-red-100 text-red-700'
    case 'medium':
      return 'bg-yellow-100 text-yellow-700'
    case 'low':
      return 'bg-green-100 text-green-700'
    default:
      return 'bg-gray-100 text-gray-700'
  }
}
</script>
