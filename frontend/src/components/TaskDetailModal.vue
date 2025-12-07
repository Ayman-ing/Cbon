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
          v-if="show && task"
          class="bg-white rounded-lg shadow-xl max-w-2xl w-full overflow-hidden"
        >
          <!-- Modal Header -->
          <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <h2 class="text-xl font-bold text-gray-900">Task Details</h2>
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
          <div class="p-6">
            <div class="space-y-6">
              <!-- Title -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Task Title
                </label>
                <input
                  v-model="editedTask.title"
                  type="text"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <!-- Description -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  v-model="editedTask.description"
                  rows="4"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                ></textarea>
              </div>

              <!-- Status -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Status
                </label>
                <select
                  v-model="editedTask.status"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="not_started">Not Started</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                </select>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <!-- Priority -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Priority
                  </label>
                  <select
                    v-model="editedTask.priority"
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>

                <!-- Assigned To -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Assign To
                  </label>
                  <input
                    v-model="editedTask.assignedTo"
                    type="text"
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex flex-col sm:flex-row gap-3 mt-8">
              <button
                @click="handleDelete"
                class="px-6 py-2.5 border border-red-300 text-red-700 rounded-lg font-medium hover:bg-red-50 transition"
              >
                Delete Task
              </button>
              <div class="flex-1"></div>
              <button
                @click="$emit('close')"
                class="px-6 py-2.5 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 transition"
              >
                Cancel
              </button>
              <button
                @click="handleUpdate"
                class="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Task } from '@/views/ProjectDetailView.vue'

const props = defineProps<{
  show: boolean
  task: Task | null
}>()

const emit = defineEmits<{
  close: []
  update: [task: Task]
  delete: [taskId: number]
}>()

const editedTask = ref<Task>({
  id: 0,
  title: '',
  description: '',
  status: 'not_started',
  priority: 'medium',
  assignedTo: '',
  createdAt: new Date()
})

watch(() => props.task, (newTask) => {
  if (newTask) {
    editedTask.value = { ...newTask }
  }
}, { immediate: true })

const handleUpdate = () => {
  emit('update', editedTask.value)
}

const handleDelete = () => {
  if (confirm('Are you sure you want to delete this task?')) {
    emit('delete', editedTask.value.id)
  }
}
</script>
