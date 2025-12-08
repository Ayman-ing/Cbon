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
              <h2 class="text-xl font-bold text-gray-900">Add New Task</h2>
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
                  Task Title <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="formData.title"
                  type="text"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter task title"
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
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                  placeholder="Enter task description"
                ></textarea>
              </div>

              <!-- Priority Field -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Priority
                </label>
                <select
                  v-model="formData.priority"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>

              <!-- Assigned To Field -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Assign To
                </label>
                <UserSelect
                  v-model="assignedUsers"
                  label="Select users to assign"
                />
              </div>
            </div>

            <!-- Modal Footer -->
            <div class="flex flex-col sm:flex-row gap-3 mt-6">
              <button
                type="button"
                @click="$emit('close')"
                class="flex-1 px-6 py-2.5 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 transition"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="flex-1 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition"
              >
                Add Task
              </button>
            </div>
          </form>
        </div>
      </Transition>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Task } from '@/services/api'
import UserSelect from './UserSelect.vue'

defineProps<{
  show: boolean
}>()

const emit = defineEmits<{
  close: []
  save: [data: Partial<Task>]
}>()

const formData = ref({
  title: '',
  description: '',
  priority: 'medium' as 'low' | 'medium' | 'high',
})

const assignedUsers = ref<string[]>([])

const handleSubmit = () => {
  // Take the first assigned user (since backend only supports one user currently)
  const assigned_to = assignedUsers.value.length > 0 ? assignedUsers.value[0] : undefined
  
  emit('save', { 
    ...formData.value,
    assigned_to
  })
  
  // Reset form
  formData.value = {
    title: '',
    description: '',
    priority: 'medium',
  }
  assignedUsers.value = []
}
</script>
