import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Project {
  id?: string
  title: string
  description?: string
  status?: string
  start_date?: string
  due_date?: string
  owner_id?: string
  created_at?: string
  updated_at?: string
}

export interface Task {
  id?: string
  project_id: string
  title: string
  description?: string
  status?: 'not_started' | 'in_progress' | 'completed' | 'archived'
  priority?: 'low' | 'medium' | 'high'
  assigned_to?: string
  due_date?: string
  position?: string
  created_at?: string
  updated_at?: string
}

export const projectApi = {
  getAll: (params?: { skip?: number; limit?: number; status_filter?: string }) =>
    api.get<Project[]>('/projects', { params }),
  
  getById: (id: string) =>
    api.get<Project>(`/projects/${id}`),
  
  create: (data: Omit<Project, 'id' | 'created_at' | 'updated_at'>) =>
    api.post<Project>('/projects', data),
  
  update: (id: string, data: Partial<Project>) =>
    api.put<Project>(`/projects/${id}`, data),
  
  delete: (id: string, soft?: boolean) =>
    api.delete(`/projects/${id}`, { params: { soft } }),
}

export const taskApi = {
  getAll: (params?: { skip?: number; limit?: number; status_filter?: string }) =>
    api.get<Task[]>('/tasks', { params }),
  
  getByProject: (projectId: string) =>
    api.get<Task[]>('/tasks', { params: { project_id: projectId } }),
  
  getById: (id: string) =>
    api.get<Task>(`/tasks/${id}`),
  
  create: (data: Omit<Task, 'id' | 'created_at' | 'updated_at'>) =>
    api.post<Task>('/tasks', data),
  
  update: (id: string, data: Partial<Task>) =>
    api.put<Task>(`/tasks/${id}`, data),
  
  delete: (id: string, soft?: boolean) =>
    api.delete(`/tasks/${id}`, { params: { soft } }),
}

export default api
