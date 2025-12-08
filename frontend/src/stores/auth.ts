import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User, type LoginCredentials, type RegisterData } from '@/services/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const isAuthenticated = computed(() => !!token.value && !!user.value)

  // Initialize from localStorage
  const initialize = () => {
    const storedToken = localStorage.getItem('access_token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      user.value = JSON.parse(storedUser)
    }
  }

  // Login
  const login = async (credentials: LoginCredentials) => {
    try {
      loading.value = true
      error.value = null

      const response = await authApi.login(credentials)
      token.value = response.data.access_token

      // Store token
      localStorage.setItem('access_token', token.value)

      // Get user info
      const userResponse = await authApi.getCurrentUser()
      user.value = userResponse.data

      // Store user info
      localStorage.setItem('user', JSON.stringify(user.value))

      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Register
  const register = async (data: RegisterData) => {
    try {
      loading.value = true
      error.value = null

      // Register user
      await authApi.register(data)

      // Auto login after registration
      await login({ email: data.email, password: data.password })

      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Registration failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Logout
  const logout = () => {
    authApi.logout()
    user.value = null
    token.value = null
  }

  // Refresh user data
  const refreshUser = async () => {
    try {
      const response = await authApi.getCurrentUser()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(user.value))
    } catch (err) {
      console.error('Failed to refresh user:', err)
      logout()
    }
  }

  // Initialize on store creation
  initialize()

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    refreshUser,
  }
})
