<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <div class="grow py-8 sm:py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Header -->
        <div class="mb-8">
          <div class="flex items-center gap-4 mb-4">
            <router-link
              to="/projects"
              class="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 transition"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
              Back to Projects
            </router-link>
          </div>
          
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-2">{{ project?.title }}</h1>
              <p class="text-base sm:text-lg text-gray-600">{{ project?.description }}</p>
            </div>
            <button
              @click="showAddTaskModal = true"
              class="inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Add Task
            </button>
          </div>
        </div>

        <!-- Kanban Board -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Not Started Column -->
          <KanbanColumn
            title="Not Started"
            :tasks="notStartedTasks"
            status="not_started"
            bg-color="bg-gray-100"
            @task-click="openTaskDetail"
          />

          <!-- In Progress Column -->
          <KanbanColumn
            title="In Progress"
            :tasks="inProgressTasks"
            status="in_progress"
            bg-color="bg-blue-100"
            @task-click="openTaskDetail"
          />

          <!-- Completed Column -->
          <KanbanColumn
            title="Completed"
            :tasks="completedTasks"
            status="completed"
            bg-color="bg-green-100"
            @task-click="openTaskDetail"
          />
        </div>
      </div>
    </div>

    <!-- Add Task Modal -->
    <TaskModal
      v-if="showAddTaskModal"
      :show="showAddTaskModal"
      @close="showAddTaskModal = false"
      @save="handleAddTask"
    />

    <!-- Task Detail Modal -->
    <TaskDetailModal
      v-if="showTaskDetailModal"
      :show="showTaskDetailModal"
      :task="selectedTask"
      @close="showTaskDetailModal = false"
      @update="handleUpdateTask"
      @delete="handleDeleteTask"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { projectApi, taskApi, type Project, type Task } from '@/services/api'
import KanbanColumn from '@/components/KanbanColumn.vue'
import TaskModal from '@/components/TaskModal.vue'
import TaskDetailModal from '@/components/TaskDetailModal.vue'

const route = useRoute()
const projectId = String(route.params.id)

const project = ref<Project | null>(null)
const tasks = ref<Task[]>([])
const showAddTaskModal = ref(false)
const showTaskDetailModal = ref(false)
const selectedTask = ref<Task | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

// Computed tasks by status
const notStartedTasks = computed(() => tasks.value.filter(t => t.status === 'not_started'))
const inProgressTasks = computed(() => tasks.value.filter(t => t.status === 'in_progress'))
const completedTasks = computed(() => tasks.value.filter(t => t.status === 'completed'))

// Load project details
const loadProject = async () => {
  try {
    const response = await projectApi.getById(projectId)
    project.value = response.data
  } catch (err) {
    console.error('Failed to load project:', err)
    error.value = 'Failed to load project details'
  }
}

// Load tasks for this project
const loadTasks = async () => {
  try {
    loading.value = true
    const response = await taskApi.getByProject(projectId)
    tasks.value = response.data
  } catch (err) {
    console.error('Failed to load tasks:', err)
    error.value = 'Failed to load tasks'
  } finally {
    loading.value = false
  }
}

const openTaskDetail = (task: Task) => {
  selectedTask.value = task
  showTaskDetailModal.value = true
}

const handleAddTask = async (taskData: Partial<Task>) => {
  try {
    const newTask: any = {
      title: taskData.title,
      description: taskData.description,
      project_id: projectId,
      status: 'not_started',
      priority: taskData.priority || 'medium',
    }
    
    // Only include assigned_to if it's a valid value (not empty string or undefined)
    if (taskData.assigned_to && taskData.assigned_to !== '') {
      newTask.assigned_to = taskData.assigned_to
    }
    
    await taskApi.create(newTask)
    await loadTasks() // Reload tasks
    showAddTaskModal.value = false
  } catch (err) {
    console.error('Failed to create task:', err)
    error.value = 'Failed to create task'
  }
}

const handleUpdateTask = async (updatedTask: Task) => {
  try {
    if (!updatedTask.id) return
    await taskApi.update(updatedTask.id, updatedTask)
    await loadTasks() // Reload tasks
    showTaskDetailModal.value = false
  } catch (err) {
    console.error('Failed to update task:', err)
    error.value = 'Failed to update task'
  }
}

const handleDeleteTask = async (taskId: string) => {
  try {
    if (!confirm('Are you sure you want to delete this task?')) return
    await taskApi.delete(taskId, false)
    await loadTasks() // Reload tasks
    showTaskDetailModal.value = false
  } catch (err) {
    console.error('Failed to delete task:', err)
    error.value = 'Failed to delete task'
  }
}

onMounted(() => {
  loadProject()
  loadTasks()
})
</script>
