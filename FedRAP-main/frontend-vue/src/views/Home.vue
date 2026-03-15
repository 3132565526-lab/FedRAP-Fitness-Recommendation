<template>
  <div class="home-view">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="stat-card">
          <el-statistic title="训练次数" :value="stats.totalWorkouts">
            <template #prefix>
              <el-icon color="#667eea"><Trophy /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <el-statistic title="消耗卡路里" :value="stats.totalCalories">
            <template #prefix>
              <el-icon color="#f56c6c"><CoffeeCup /></el-icon>
            </template>
            <template #suffix>kcal</template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <el-statistic title="当前等级" :value="userLevel">
            <template #prefix>
              <el-icon color="#67c23a"><Medal /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>个人信息</span>
            </div>
          </template>
          <div v-if="userProfile" class="user-info">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="年龄">{{ userProfile.age || '-' }}</el-descriptions-item>
              <el-descriptions-item label="性别">{{ genderText }}</el-descriptions-item>
              <el-descriptions-item label="身高">{{ userProfile.height || '-' }} cm</el-descriptions-item>
              <el-descriptions-item label="体重">{{ userProfile.weight || '-' }} kg</el-descriptions-item>
              <el-descriptions-item label="BMI">{{ userProfile.bmi?.toFixed(1) || '-' }}</el-descriptions-item>
              <el-descriptions-item label="健身水平">{{ fitnessLevelText }}</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>健身目标</span>
            </div>
          </template>
          <div v-if="userProfile" class="goals">
            <div class="goal-item">
              <span>减脂</span>
              <el-progress :percentage="(userProfile.goalWeightLoss || 0) * 100" color="#f56c6c" />
            </div>
            <div class="goal-item">
              <span>增肌</span>
              <el-progress :percentage="(userProfile.goalMuscleGain || 0) * 100" color="#67c23a" />
            </div>
            <div class="goal-item">
              <span>耐力</span>
              <el-progress :percentage="(userProfile.goalEndurance || 0) * 100" color="#409eff" />
            </div>
            <div class="goal-item">
              <span>柔韧性</span>
              <el-progress :percentage="(userProfile.goalFlexibility || 0) * 100" color="#e6a23c" />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>快速开始</span>
            </div>
          </template>
          <div class="quick-actions">
            <el-button type="primary" size="large" @click="goTo('/dashboard/recommendation')">
              <el-icon><MagicStick /></el-icon>
              获取智能推荐
            </el-button>
            <el-button type="success" size="large" @click="goTo('/dashboard/training')">
              <el-icon><Timer /></el-icon>
              开始训练
            </el-button>
            <el-button type="info" size="large" @click="goTo('/dashboard/exercises')">
              <el-icon><Trophy /></el-icon>
              浏览动作库
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { userService, trainingService } from '@/services'
import { Trophy, CoffeeCup, Medal, MagicStick, Timer } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const userProfile = ref(null)
const stats = ref({
  totalWorkouts: 0,
  totalCalories: 0
})

const userLevel = computed(() => userProfile.value?.level || 1)

const genderText = computed(() => {
  const genderMap = { MALE: '男', FEMALE: '女', OTHER: '其他' }
  return genderMap[userProfile.value?.gender] || '-'
})

const fitnessLevelText = computed(() => {
  const level = userProfile.value?.fitnessLevel || 0
  if (level < 0.3) return '初级'
  if (level < 0.7) return '中级'
  return '高级'
})

const fetchData = async () => {
  try {
    const userRes = await userService.getCurrentUser()
    if (userRes.data.code === 200) {
      userProfile.value = userRes.data.data
    }

    const statsRes = await trainingService.getTrainingStats(authStore.user.id)
    if (statsRes.data.code === 200) {
      stats.value = statsRes.data.data
    }
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

const goTo = (path) => {
  router.push(path)
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.home-view {
  max-width: 1400px;
  margin: 0 auto;
}

.stat-card {
  text-align: center;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.user-info {
  padding: 10px 0;
}

.goals {
  padding: 10px 0;
}

.goal-item {
  margin-bottom: 20px;
}

.goal-item:last-child {
  margin-bottom: 0;
}

.goal-item span {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #606266;
}

.quick-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  padding: 20px;
}
</style>
