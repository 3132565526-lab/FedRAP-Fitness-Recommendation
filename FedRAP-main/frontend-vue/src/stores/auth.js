import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)

  async function login(username, password) {
    const response = await api.post('/auth/login', { username, password })
    if (response.data.code === 200) {
      const data = response.data.data
      token.value = data.token
      user.value = {
        id: data.userId,
        username: data.username,
        email: data.email,
        role: data.role
      }
      localStorage.setItem('token', data.token)
      localStorage.setItem('user', JSON.stringify(user.value))
      return true
    }
    return false
  }

  async function register(registerData) {
    const response = await api.post('/auth/register', registerData)
    if (response.data.code === 200) {
      const data = response.data.data
      token.value = data.token
      user.value = {
        id: data.userId,
        username: data.username,
        email: data.email,
        role: data.role
      }
      localStorage.setItem('token', data.token)
      localStorage.setItem('user', JSON.stringify(user.value))
      return true
    }
    return false
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  async function fetchCurrentUser() {
    try {
      const response = await api.get('/users/me')
      if (response.data.code === 200) {
        const userData = response.data.data
        user.value = { ...user.value, ...userData }
        localStorage.setItem('user', JSON.stringify(user.value))
      }
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    fetchCurrentUser
  }
})
