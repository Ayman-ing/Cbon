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
import { projectApi, type Project } from '@/services/api'
import KanbanColumn from '@/components/KanbanColumn.vue'
import TaskModal from '@/components/TaskModal.vue'
import TaskDetailModal from '@/components/TaskDetailModal.vue'

export interface Task {
  id: number
  title: string
  description: string
  status: 'not_started' | 'in_progress' | 'completed'
  assignedTo?: string
  priority: 'low' | 'medium' | 'high'
  createdAt: Date
}

const route = useRoute()
const projectId = String(route.params.id)

const project = ref<Project | null>(null)
const tasks = ref<Task[]>([])
const showAddTaskModal = ref(false)
const showTaskDetailModal = ref(false)
const selectedTask = ref<Task | null>(null)

// Computed tasks by status
const notStartedTasks = computed(() => tasks.value.filter(t => t.status === 'not_started'))
const inProgressTasks = computed(() => tasks.value.filter(t => t.status === 'in_progress'))
const completedTasks = computed(() => tasks.value.filter(t => t.status === 'completed'))

// Load project details
const loadProject = async () => {
  try {
    const response = await projectApi.getById(projectId)
    project.value = response.data
  } catch (error) {
    console.error('Failed to load project:', error)
  }
}

// Mock tasks for now (will be replaced with API calls)
const loadTasks = () => {
  tasks.value = [
    {
      id: 1,
      title: 'Design homepage mockup',
      description: 'Create initial design mockups for the homepage',
      status: 'completed',
      assignedTo: 'John Doe',
      priority: 'high',
      createdAt: new Date('2025-12-01')
    },
    {
      id: 2,
      title: 'Implement authentication',
      description: 'Set up user authentication system with JWT',
      status: 'in_progress',
      assignedTo: 'Jane Smith',
      priority: 'high',
      createdAt: new Date('2025-12-03')
    },
    {
      id: 3,
      title: 'Write API documentation',
      description: 'Document all API endpoints and request/response formats',
      status: 'not_started',
      priority: 'medium',
      createdAt: new Date('2025-12-05')
    },
  ]
}

const openTaskDetail = (task: Task) => {
  selectedTask.value = task
  showTaskDetailModal.value = true
}

const handleAddTask = (taskData: Partial<Task>) => {
  // TODO: Call API to create task
  const newTask: Task = {
    id: tasks.value.length + 1,
    title: taskData.title!,
    description: taskData.description || '',
    status: 'not_started',
    assignedTo: taskData.assignedTo,
    priority: taskData.priority || 'medium',
    createdAt: new Date()
  }
  tasks.value.push(newTask)
  showAddTaskModal.value = false
}

const handleUpdateTask = (updatedTask: Task) => {
  // TODO: Call API to update task
  const index = tasks.value.findIndex(t => t.id === updatedTask.id)
  if (index !== -1) {
    tasks.value[index] = updatedTask
  }
  showTaskDetailModal.value = false
}

const handleDeleteTask = (taskId: number) => {
  // TODO: Call API to delete task
  tasks.value = tasks.value.filter(t => t.id !== taskId)
  showTaskDetailModal.value = false
}

onMounted(() => {
  loadProject()
  loadTasks()
})
</script>
