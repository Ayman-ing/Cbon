<template>
  <Transition
    enter-active-class="transition ease-out duration-200"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition ease-in duration-150"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="show"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="$emit('close')"
    >
      <Transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 scale-95"
        enter-to-class="opacity-100 scale-100"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-95"
      >
        <div
          v-if="show"
          class="bg-white rounded-lg shadow-xl max-w-lg w-full overflow-hidden"
        >
          <!-- Modal Header -->
          <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <h2 class="text-xl font-bold text-gray-900">
                {{ project ? 'Edit Project' : 'Create New Project' }}
              </h2>
              <button
                @click="$emit('close')"
                class="text-gray-400 hover:text-gray-600 transition"
              >
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Modal Body -->
          <form @submit.prevent="handleSubmit" class="p-6">
            <div class="space-y-5">
              <!-- Title Field -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Project Title <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="formData.title"
                  type="text"
                  required
                  class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                  placeholder="e.g., Website Redesign"
                />
              </div>

              <!-- Description Field -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  v-model="formData.description"
                  rows="4"
                  class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition resize-none"
                  placeholder="Provide a brief description of your project..."
                ></textarea>
              </div>

              <!-- Status Field -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Status
                </label>
                <select
                  v-model="formData.status"
                  class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition bg-white"
                >
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                  <option value="on-hold">On Hold</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>

              <!-- Date Fields Row -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <!-- Start Date Field -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Start Date
                  </label>
                  <input
                    v-model="formData.start_date"
                    type="date"
                    class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                  />
                </div>

                <!-- Due Date Field -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Due Date
                  </label>
                  <input
                    v-model="formData.due_date"
                    type="date"
                    class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                  />
                </div>
              </div>
            </div>

            <!-- Modal Footer -->
            <div class="mt-6 flex gap-3">
              <button
                type="button"
                @click="$emit('close')"
                class="flex-1 px-4 py-2.5 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="saving"
                class="flex-1 px-4 py-2.5 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ saving ? 'Saving...' : (project ? 'Update Project' : 'Create Project') }}
              </button>
            </div>
          </form>
        </div>
      </Transition>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Project } from '@/services/api'

const props = defineProps<{
  show: boolean
  project?: Project | null
  saving: boolean
}>()

const emit = defineEmits<{
  close: []
  save: [data: Partial<Project>]
}>()

const formData = ref({
  title: '',
  description: '',
  status: 'active',
  start_date: '',
  due_date: '',
})

watch(() => props.project, (project) => {
  if (project) {
    formData.value = {
      title: project.title,
      description: project.description || '',
      status: project.status || 'active',
      start_date: project.start_date || '',
      due_date: project.due_date || '',
    }
  } else {
    formData.value = {
      title: '',
      description: '',
      status: 'active',
      start_date: '',
      due_date: '',
    }
  }
}, { immediate: true })

const handleSubmit = () => {
  emit('save', formData.value)
}
</script>
