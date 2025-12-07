<template>
  <div class="flex flex-col">
    <!-- Hero Section -->
    <div class="w-full bg-linear-to-br from-blue-50 to-indigo-100 py-16 sm:py-20 lg:py-24 px-6 sm:px-8 lg:px-12 mb-12 sm:mb-16 lg:mb-20">
      <div class="max-w-7xl mx-auto">
        <div class="flex flex-col items-center justify-center text-center space-y-8">
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900">
            Welcome to <span class="text-blue-600">Cbon</span>
          </h1>
          <p class="text-lg sm:text-xl text-gray-600 max-w-2xl">
            Your powerful project management solution. Organize, track, and deliver projects with ease.
          </p>
          
          <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mt-8">
            <router-link
              to="/projects"
              class="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium transition"
            >
              Get Started
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </router-link>
            <button
              @click="scrollToFeatures"
              class="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-white hover:bg-gray-50 text-gray-700 px-8 py-3 rounded-lg font-medium border border-gray-200 transition"
            >
              Learn More
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div ref="featuresRef" class="w-full py-16 sm:py-20 lg:py-24 px-6 sm:px-8 lg:px-12 bg-gray-50 mb-12 sm:mb-16 lg:mb-20">
      <div class="max-w-7xl mx-auto">
        <div class="flex flex-col items-center justify-center text-center mb-12 space-y-4">
          <h2 class="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900">
            Why Choose Cbon?
          </h2>
          <p class="text-lg sm:text-xl text-gray-600 max-w-2xl">
            Everything you need to manage your projects efficiently
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <div
            v-for="feature in features"
            :key="feature.title"
            class="flex flex-col items-center justify-start text-center p-8 bg-white rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-lg transition"
          >
            <div class="text-4xl mb-4">{{ feature.icon }}</div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3">
              {{ feature.title }}
            </h3>
            <p class="text-base text-gray-600">
              {{ feature.description }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="w-full bg-blue-600 py-16 sm:py-20 lg:py-24 px-6 sm:px-8 lg:px-12">
      <div class="max-w-7xl mx-auto">
        <div class="flex flex-col items-center justify-center text-center space-y-8">
          <h2 class="text-3xl sm:text-4xl lg:text-5xl font-bold text-white">
            Ready to Get Started?
          </h2>
          <p class="text-lg sm:text-xl text-blue-100 max-w-2xl">
            Join thousands of teams managing their projects with Cbon
          </p>
          <router-link
            to="/projects"
            class="inline-flex items-center justify-center gap-2 bg-white hover:bg-gray-100 text-blue-600 px-8 py-3 rounded-lg font-medium transition"
          >
            View Your Projects
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { projectApi } from '@/services/api'

const featuresRef = ref<HTMLElement | null>(null)

const stats = ref({
  projects: 0,
  active: 0,
  completed: 0,
})

const features = [
  {
    icon: '🚀',
    title: 'Easy to Use',
    description: 'Intuitive interface that gets you started in minutes, not hours.',
  },
  {
    icon: '📊',
    title: 'Track Progress',
    description: 'Monitor project status and completion in real-time with detailed insights.',
  },
  {
    icon: '🔒',
    title: 'Secure & Reliable',
    description: 'Your data is safe with enterprise-grade security and regular backups.',
  },
  {
    icon: '⚡',
    title: 'Fast Performance',
    description: 'Lightning-fast response times ensure smooth workflow without delays.',
  },
  {
    icon: '🤝',
    title: 'Team Collaboration',
    description: 'Work together seamlessly with your team on shared projects.',
  },
  {
    icon: '📱',
    title: 'Responsive Design',
    description: 'Access your projects anywhere, on any device, at any time.',
  },
]

const scrollToFeatures = () => {
  featuresRef.value?.scrollIntoView({ behavior: 'smooth' })
}

const loadStats = async () => {
  try {
    const response = await projectApi.getAll({ skip: 0, limit: 1000 })
    const projects = response.data

    stats.value = {
      projects: projects.length,
      active: projects.filter((p) => p.is_active).length,
      completed: projects.filter((p) => p.status === 'completed').length,
    }
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

onMounted(() => {
  loadStats()
})
</script>
