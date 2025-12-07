<template>
  <div
    class="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-lg hover:border-blue-200 transition-all duration-200 overflow-hidden flex flex-col h-full cursor-pointer"
    @click="navigateToDetail"
  >
    <!-- Card Header -->
    <div class="p-4 sm:p-6 pb-3 sm:pb-4 flex-grow">
      <div class="flex items-start justify-between gap-3 mb-3">
        <h3 class="text-base sm:text-lg font-semibold text-gray-900 flex-1 line-clamp-2">
          {{ project.title }}
        </h3>
        <span
          :class="[
            'flex-shrink-0 px-2 sm:px-2.5 py-1 text-xs font-medium rounded-full whitespace-nowrap',
            project.status === 'active'
              ? 'bg-green-100 text-green-800'
              : 'bg-gray-100 text-gray-600'
          ]"
        >
          {{ project.status }}
        </span>
      </div>

      <!-- Description -->
      <p class="text-sm text-gray-600 line-clamp-3 min-h-[3.5rem]">
        {{ project.description || 'No description provided' }}
      </p>
    </div>

    <!-- Card Footer -->
    <div class="px-4 sm:px-6 py-3 sm:py-4 bg-gray-50 border-t border-gray-100 mt-auto">
      <div class="flex flex-col gap-2 mb-3">
        <!-- Created Date -->
        <div class="flex items-center text-xs text-gray-500">
          <svg class="w-4 h-4 mr-1.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span class="truncate">Created: {{ formatDate(project.created_at) }}</span>
        </div>
        
        <!-- Due Date -->
        <div v-if="project.due_date" class="flex items-center text-xs text-gray-500">
          <svg class="w-4 h-4 mr-1.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="truncate">Due: {{ formatDate(project.due_date) }}</span>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-2">
        <button
          @click.stop="$emit('edit', project)"
          class="flex-1 inline-flex items-center justify-center gap-1 sm:gap-1.5 bg-white hover:bg-gray-100 text-gray-700 px-2 sm:px-3 py-2 rounded-md text-xs sm:text-sm font-medium border border-gray-300 transition"
        >
          <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          <span class="hidden sm:inline">Edit</span>
        </button>
        <button
          @click.stop="$emit('delete', project.id!)"
          class="flex-1 inline-flex items-center justify-center gap-1 sm:gap-1.5 bg-red-50 hover:bg-red-100 text-red-600 px-2 sm:px-3 py-2 rounded-md text-xs sm:text-sm font-medium border border-red-200 transition"
        >
          <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          <span class="hidden sm:inline">Delete</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Project } from '@/services/api'

const props = defineProps<{
  project: Project
}>()

defineEmits<{
  click: [project: Project]
  edit: [project: Project]
  delete: [id: string]
}>()

const router = useRouter()

const navigateToDetail = () => {
  router.push(`/projects/${props.project.id}`)
}

const formatDate = (date?: string) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}
</script>
