<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
    <ProjectCard
      v-for="project in projects"
      :key="project.id"
      :project="project"
      @edit="$emit('edit', project)"
      @delete="(id: string) => $emit('delete', id)"
    />
  </div>
</template>

<script setup lang="ts">
import type { Project } from '@/services/api'
import ProjectCard from './ProjectCard.vue'

defineProps<{
  projects: Project[]
}>()

defineEmits<{
  edit: [project: Project]
  delete: [id: string]
}>()
</script>
