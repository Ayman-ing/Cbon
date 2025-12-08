<template>
  <div class="relative">
    <label v-if="label" class="block text-sm font-medium text-gray-700 mb-2">
      {{ label }}
    </label>
    
    <div class="relative">
      <!-- Input Field -->
      <div
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500 bg-white cursor-text"
        @click="focusInput"
      >
        <!-- Selected Users -->
        <div class="flex flex-wrap gap-2 mb-1" v-if="selectedUsers.length > 0">
          <span
            v-for="user in selectedUsers"
            :key="user.id"
            class="inline-flex items-center gap-1 bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm"
          >
            <span class="w-5 h-5 rounded-full bg-blue-600 text-white flex items-center justify-center text-xs font-medium">
              {{ user.full_name.charAt(0).toUpperCase() }}
            </span>
            {{ user.full_name }}
            <button
              type="button"
              @click.stop="removeUser(user.id)"
              class="ml-1 hover:bg-blue-200 rounded-full p-0.5"
            >
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </span>
        </div>
        
        <!-- Search Input -->
        <input
          ref="searchInput"
          v-model="searchQuery"
          type="text"
          placeholder="Search users..."
          class="w-full outline-none text-sm"
          @focus="showDropdown = true"
          @input="handleSearch"
        />
      </div>

      <!-- Dropdown -->
      <div
        v-if="showDropdown && (filteredUsers.length > 0 || loading)"
        class="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-auto"
      >
        <!-- Loading State -->
        <div v-if="loading" class="px-4 py-3 text-sm text-gray-500 text-center">
          Searching...
        </div>

        <!-- User List -->
        <div v-else>
          <button
            v-for="user in filteredUsers"
            :key="user.id"
            type="button"
            @click="selectUser(user)"
            class="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-3 transition"
            :class="{ 'bg-blue-50': isSelected(user.id) }"
          >
            <div class="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-medium">
              {{ user.full_name.charAt(0).toUpperCase() }}
            </div>
            <div class="flex-1">
              <div class="text-sm font-medium text-gray-900">{{ user.full_name }}</div>
              <div class="text-xs text-gray-500">{{ user.email }}</div>
            </div>
            <svg
              v-if="isSelected(user.id)"
              class="w-5 h-5 text-blue-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </button>
        </div>

        <!-- No Results -->
        <div
          v-if="!loading && searchQuery.length > 0 && filteredUsers.length === 0"
          class="px-4 py-3 text-sm text-gray-500 text-center"
        >
          No users found
        </div>
      </div>
    </div>

    <!-- Click Outside Handler -->
    <div
      v-if="showDropdown"
      class="fixed inset-0 z-40"
      @click="showDropdown = false"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { userApi, type User } from '@/services/auth'

const props = defineProps<{
  modelValue: string[]  // Array of user IDs
  label?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string[]]
}>()

const searchInput = ref<HTMLInputElement | null>(null)
const searchQuery = ref('')
const showDropdown = ref(false)
const loading = ref(false)
const allUsers = ref<User[]>([])

// Selected users
const selectedUsers = computed(() => {
  return allUsers.value.filter(user => user.id && props.modelValue.includes(user.id))
})

// Filtered users based on search
const filteredUsers = computed(() => {
  if (searchQuery.value.length === 0) {
    return []
  }
  
  const query = searchQuery.value.toLowerCase()
  return allUsers.value.filter(user => {
    const matchesSearch = 
      user.full_name.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query)
    
    // Don't show already selected users
    const notSelected = !props.modelValue.includes(user.id!)
    
    return matchesSearch && notSelected
  })
})

// Load users
const loadUsers = async () => {
  try {
    loading.value = true
    const response = await userApi.getAll({ limit: 100 })
    allUsers.value = response.data
  } catch (error) {
    console.error('Failed to load users:', error)
  } finally {
    loading.value = false
  }
}

// Handle search input
const handleSearch = () => {
  if (searchQuery.value.length >= 1) {
    showDropdown.value = true
    if (allUsers.value.length === 0) {
      loadUsers()
    }
  } else {
    showDropdown.value = false
  }
}

// Select user
const selectUser = (user: User) => {
  if (user.id && !props.modelValue.includes(user.id)) {
    emit('update:modelValue', [...props.modelValue, user.id])
  }
  searchQuery.value = ''
  showDropdown.value = false
}

// Remove user
const removeUser = (userId: string) => {
  emit('update:modelValue', props.modelValue.filter(id => id !== userId))
}

// Check if user is selected
const isSelected = (userId?: string) => {
  return userId ? props.modelValue.includes(userId) : false
}

// Focus input
const focusInput = () => {
  searchInput.value?.focus()
}

// Watch for when users are selected to load their data
watch(() => props.modelValue, () => {
  if (props.modelValue.length > 0 && allUsers.value.length === 0) {
    loadUsers()
  }
}, { immediate: true })

onMounted(() => {
  // Pre-load users if there are selected values
  if (props.modelValue.length > 0) {
    loadUsers()
  }
})
</script>
