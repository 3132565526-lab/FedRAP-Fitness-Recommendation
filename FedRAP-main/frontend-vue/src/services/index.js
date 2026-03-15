import api from './api'

export const userService = {
  // 获取当前用户信息
  getCurrentUser() {
    return api.get('/users/me')
  },

  // 获取用户信息
  getUserById(userId) {
    return api.get(`/users/${userId}`)
  },

  // 更新用户资料
  updateProfile(userId, data) {
    return api.put(`/users/${userId}`, data)
  }
}

export const exerciseService = {
  // 获取所有动作
  getAllExercises() {
    return api.get('/exercises/list')
  },

  // 获取动作详情
  getExerciseById(exerciseId) {
    return api.get(`/exercises/${exerciseId}`)
  },

  // 按类别获取动作
  getExercisesByCategory(category) {
    return api.get(`/exercises/category/${category}`)
  }
}

export const recommendationService = {
  // 获取推荐
  getRecommendations(data) {
    return api.post('/recommendations', data)
  },

  // 获取用户推荐
  getUserRecommendations(userId, topK = 10) {
    return api.get(`/recommendations/user/${userId}?topK=${topK}`)
  }
}

export const trainingService = {
  // 记录训练
  recordTraining(data) {
    return api.post('/training/record', data)
  },

  // 获取训练历史
  getTrainingHistory(userId) {
    return api.get(`/training/history/${userId}`)
  },

  // 获取训练统计
  getTrainingStats(userId) {
    return api.get(`/training/stats/${userId}`)
  }
}

export const workoutPlanService = {
  // 获取用户当前训练计划
  getActivePlan(userId) {
    return api.get(`/plans/active/${userId}`)
  },

  // 加入训练计划
  addPlanItem(data) {
    return api.post('/plans/items', data)
  },

  // 移除训练计划条目
  removePlanItem(planId, exerciseId, userId) {
    const userQuery = userId ? `?userId=${userId}` : ''
    return api.delete(`/plans/${planId}/items/${exerciseId}${userQuery}`)
  }
}
