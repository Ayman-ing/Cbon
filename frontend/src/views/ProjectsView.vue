<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <div class="grow py-8 sm:py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Header Section -->
        <div class="mb-8">
          <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-2">Projects</h1>
          <p class="text-base sm:text-lg text-gray-600">Manage your project portfolio</p>
        </div>

        <!-- Actions Bar -->
        <div class="mb-8">
          <ProjectActions
            v-model:active-only="activeOnly"
            @create="openCreateModal"
          />
        </div>

        <!-- Content Area -->
        <div>
          <!-- Loading State -->
          <div v-if="loading" class="flex flex-col items-center justify-center py-20 bg-white rounded-lg">
            <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
            <p class="mt-4 text-base text-gray-600">Loading projects...</p>
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6">
            <div class="flex items-start gap-3">
              <svg class="h-5 w-5 text-red-400 mt-0.5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
              <div>
                <h3 class="text-sm font-medium text-red-800">Error loading projects</h3>
                <p class="mt-1 text-sm text-red-700">{{ error }}</p>
              </div>
            </div>
          </div>

          <!-- Projects List -->
          <div v-else-if="projects.length > 0">
            <ProjectList
              :projects="projects"
              @edit="openEditModal"
              @delete="deleteProject"
            />
          </div>

          <!-- Empty State -->
          <div v-else class="bg-white rounded-lg border-2 border-dashed border-gray-300 py-20">
            <div class="flex flex-col items-center justify-center text-center px-4">
              <svg class="h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
              </svg>
              <h3 class="mt-4 text-lg font-medium text-gray-900">No projects found</h3>
              <p class="mt-2 text-base text-gray-500">Get started by creating your first project.</p>
              <div class="mt-6">
                <button
                  @click="openCreateModal"
                  class="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition"
                >
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Create your first project
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <ProjectModal
      :show="showModal"
      :project="editingProject"
      :saving="saving"
      @close="closeModal"
      @save="saveProject"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { projectApi, type Project } from '@/services/api'
import ProjectActions from '@/components/ProjectActions.vue'
import ProjectList from '@/components/ProjectList.vue'
import ProjectModal from '@/components/ProjectModal.vue'

const projects = ref<Project[]>([])
const loading = ref(false)
const error = ref('')
const activeOnly = ref(false)

const showModal = ref(false)
const editingProject = ref<Project | null>(null)
const saving = ref(false)

const loadProjects = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await projectApi.getAll({
      skip: 0,
      limit: 100,
      status_filter: activeOnly.value ? 'active' : undefined,
    })
    projects.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load projects'
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editingProject.value = null
  showModal.value = true
}

const openEditModal = (project: Project) => {
  editingProject.value = project
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingProject.value = null
}

const saveProject = async (data: Partial<Project>) => {
  saving.value = true
  try {
    if (editingProject.value) {
      await projectApi.update(editingProject.value.id!, data)
    } else {
      await projectApi.create(data as Omit<Project, 'id' | 'created_at' | 'updated_at'>)
    }
    closeModal()
    loadProjects()
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to save project'
  } finally {
    saving.value = false
  }
}

const deleteProject = async (id: string) => {
  if (!confirm('Are you sure you want to delete this project?')) return

  try {
    await projectApi.delete(id, false)
    loadProjects()
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to delete project'
  }
}

watch(activeOnly, () => {
  loadProjects()
})

onMounted(() => {
  loadProjects()
})
</script>
