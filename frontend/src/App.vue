<script setup lang="ts">
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <div class="flex items-center">
            <router-link to="/" class="flex items-center gap-2">
              <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span class="text-white font-bold text-lg">C</span>
              </div>
              <h1 class="text-xl font-bold text-gray-900">Cbon</h1>
            </router-link>
          </div>
          
          <!-- Navigation -->
          <nav class="flex items-center gap-2 sm:gap-4">
            <RouterLink 
              to="/" 
              class="text-gray-600 hover:text-gray-900 hover:bg-gray-50 px-3 py-2 rounded-md text-sm font-medium transition"
              active-class="text-blue-600 bg-blue-50"
            >
              Home
            </RouterLink>
            <RouterLink 
              v-if="authStore.isAuthenticated"
              to="/projects" 
              class="text-gray-600 hover:text-gray-900 hover:bg-gray-50 px-3 py-2 rounded-md text-sm font-medium transition"
              active-class="text-blue-600 bg-blue-50"
            >
              Projects
            </RouterLink>

            <!-- Auth Section -->
            <div v-if="authStore.isAuthenticated" class="flex items-center gap-3 ml-4 pl-4 border-l border-gray-200">
              <div class="hidden sm:flex items-center gap-2">
                <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-medium text-sm">
                  {{ authStore.user?.full_name?.charAt(0).toUpperCase() }}
                </div>
                <span class="text-sm text-gray-700">{{ authStore.user?.full_name }}</span>
              </div>
              <button
                @click="handleLogout"
                class="text-gray-600 hover:text-gray-900 hover:bg-gray-50 px-3 py-2 rounded-md text-sm font-medium transition"
              >
                Logout
              </button>
            </div>

            <div v-else class="flex items-center gap-2 ml-4 pl-4 border-l border-gray-200">
              <RouterLink 
                to="/login" 
                class="text-gray-600 hover:text-gray-900 hover:bg-gray-50 px-3 py-2 rounded-md text-sm font-medium transition"
              >
                Login
              </RouterLink>
              <RouterLink 
                to="/register" 
                class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition"
              >
                Sign up
              </RouterLink>
            </div>
          </nav>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow">
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-300 mt-auto">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <!-- About Section -->
          <div>
            <h3 class="text-white font-semibold text-lg mb-4">Cbon</h3>
            <p class="text-sm text-gray-400">
              Your powerful project management solution. Organize, track, and deliver projects with ease.
            </p>
          </div>

          <!-- Quick Links -->
          <div>
            <h3 class="text-white font-semibold text-lg mb-4">Quick Links</h3>
            <ul class="space-y-2">
              <li>
                <router-link to="/" class="text-sm text-gray-400 hover:text-white transition">
                  Home
                </router-link>
              </li>
              <li v-if="authStore.isAuthenticated">
                <router-link to="/projects" class="text-sm text-gray-400 hover:text-white transition">
                  Projects
                </router-link>
              </li>
            </ul>
          </div>

          <!-- Contact Info -->
          <div>
            <h3 class="text-white font-semibold text-lg mb-4">Contact</h3>
            <ul class="space-y-2 text-sm text-gray-400">
              <li>Email: info@cbon.com</li>
              <li>Phone: +1 (555) 123-4567</li>
            </ul>
          </div>
        </div>

        <!-- Bottom Bar -->
        <div class="border-t border-gray-800 pt-6">
          <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
            <p class="text-sm text-gray-400">
              © {{ new Date().getFullYear() }} Cbon. All rights reserved.
            </p>
            <div class="flex gap-6">
              <a href="#" class="text-sm text-gray-400 hover:text-white transition">Privacy Policy</a>
              <a href="#" class="text-sm text-gray-400 hover:text-white transition">Terms of Service</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>
