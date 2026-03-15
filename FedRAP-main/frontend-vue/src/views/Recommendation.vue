<template>
  <div class="recommendation-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>智能推荐 - 为您量身定制</span>
          <el-button type="primary" @click="fetchRecommendations" :loading="loading">
            <el-icon><Refresh /></el-icon>
            刷新推荐
          </el-button>
        </div>
      </template>

      <el-row :gutter="20" v-loading="loading">
        <el-col :span="8" v-for="item in recommendations" :key="item.exerciseId">
          <el-card class="exercise-card" shadow="hover">
            <div class="exercise-score">
              <el-tag type="success">推荐度: {{ (item.score * 100).toFixed(0) }}%</el-tag>
            </div>
            <h3>{{ item.exerciseName }}</h3>
            <p class="category">{{ item.category }} | {{ item.targetMuscle }}</p>
            <el-divider />
            <div class="exercise-details">
              <div><strong>难度:</strong> {{ (item.difficulty * 100).toFixed(0) }}%</div>
              <div><strong>组数:</strong> {{ item.recommendedSets }} 组</div>
              <div><strong>次数:</strong> {{ item.recommendedReps }} 次/组</div>
              <div><strong>时长:</strong> {{ item.recommendedDuration }} 分钟</div>
            </div>
            <div class="card-actions">
              <el-button size="small" @click="addToPlan(item)">加入训练计划</el-button>
              <el-button type="primary" size="small" @click="startTraining(item)">开始训练</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-empty v-if="!loading && recommendations.length === 0" description="暂无推荐，请先完善个人资料" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { recommendationService, workoutPlanService } from '@/services'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()
const recommendations = ref([])
const loading = ref(false)

const fetchRecommendations = async () => {
  loading.value = true
  try {
    const res = await recommendationService.getUserRecommendations(authStore.user.id, 12)
    if (res.data.code === 200) {
      recommendations.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('获取推荐失败')
  } finally {
    loading.value = false
  }
}

const startTraining = (exercise) => {
  router.push({
    path: '/dashboard/training',
    query: { exerciseId: exercise.exerciseId }
  })
}

const addToPlan = async (exercise) => {
  try {
    const payload = {
      userId: authStore.user.id,
      exerciseId: exercise.exerciseId,
      sets: exercise.recommendedSets,
      reps: exercise.recommendedReps,
      duration: exercise.recommendedDuration
    }
    const res = await workoutPlanService.addPlanItem(payload)
    if (res.data.code === 200) {
      ElMessage.success('已加入训练计划')
    } else {
      ElMessage.error(res.data.message || '加入训练计划失败')
    }
  } catch (error) {
    ElMessage.error('加入训练计划失败')
  }
}

onMounted(() => {
  fetchRecommendations()
})
</script>

<style scoped>
.recommendation-view {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.exercise-card {
  margin-bottom: 20px;
  position: relative;
}

.exercise-score {
  position: absolute;
  top: 10px;
  right: 10px;
}

.exercise-card h3 {
  color: #2c3e50;
  margin-bottom: 5px;
}

.category {
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 10px;
}

.exercise-details {
  font-size: 14px;
  line-height: 1.8;
}

.card-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
</style>
