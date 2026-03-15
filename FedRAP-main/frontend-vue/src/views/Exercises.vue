<template>
  <div class="exercises-view">
    <el-card :body-style="{ padding: '15px' }">
      <template #header>
        <div class="card-header">
          <span style="font-weight: bold; font-size: 16px">动作库 <el-tag type="info" size="small">共{{ exercises.length }}项</el-tag></span>
          <el-input
            v-model="searchText"
            placeholder="搜索动作名称..."
            clearable
            style="width: 300px"
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </template>

      <el-table :data="filteredExercises" v-loading="loading" stripe :height="tableHeight">
        <el-table-column prop="name" label="动作名称" min-width="280" show-overflow-tooltip />
        <el-table-column label="类别" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getCategoryType(row.category)" size="small">{{ getCategoryName(row.category) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="targetMuscle" label="目标肌群" width="100" align="center" />
        <el-table-column prop="equipment" label="器械" width="100" align="center" />
        <el-table-column label="难度" width="140">
          <template #default="{ row }">
            <el-progress :percentage="(row.difficulty * 100)" :color="getDifficultyColor(row.difficulty)" :show-text="false" />
            <span style="margin-left: 5px; font-size: 12px">{{ (row.difficulty * 100).toFixed(0) }}%</span>
          </template>
        </el-table-column>
        <el-table-column label="强度" width="140">
          <template #default="{ row }">
            <el-progress :percentage="(row.intensity * 100)" :color="getIntensityColor(row.intensity)" :show-text="false" />
            <span style="margin-left: 5px; font-size: 12px">{{ (row.intensity * 100).toFixed(0) }}%</span>
          </template>
        </el-table-column>
        <el-table-column label="时长" width="80" align="center">
          <template #default="{ row }">
            {{ row.recommendedDuration }}分
          </template>
        </el-table-column>
        <el-table-column label="卡路里" width="90" align="center">
          <template #default="{ row }">
            <span style="color: #f56c6c; font-weight: bold">{{ row.caloriesPerMinute }}</span>/分
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewDetail(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="动作详情" width="700px">
      <div v-if="currentExercise" class="exercise-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="动作名称" :span="2">
            <strong style="font-size: 16px">{{ currentExercise.name }}</strong>
          </el-descriptions-item>
          
          <el-descriptions-item label="动作描述" :span="2">
            <div style="line-height: 1.8">{{ currentExercise.description }}</div>
          </el-descriptions-item>
          
          <el-descriptions-item label="运动类别">
            <el-tag :type="getCategoryType(currentExercise.category)">
              {{ getCategoryName(currentExercise.category) }}
            </el-tag>
          </el-descriptions-item>
          
          <el-descriptions-item label="目标肌群">
            <el-tag type="success">{{ currentExercise.targetMuscle }}</el-tag>
          </el-descriptions-item>
          
          <el-descriptions-item label="所需器械">
            {{ currentExercise.equipment }}
          </el-descriptions-item>
          
          <el-descriptions-item label="每分钟卡路里">
            <strong style="color: #f56c6c">{{ currentExercise.caloriesPerMinute }} 卡</strong>
          </el-descriptions-item>
          
          <el-descriptions-item label="难度等级">
            <el-progress :percentage="(currentExercise.difficulty * 100)" 
                         :color="getDifficultyColor(currentExercise.difficulty)" 
                         :stroke-width="20" />
            <span style="margin-left: 10px">{{ (currentExercise.difficulty * 100).toFixed(0) }}%</span>
          </el-descriptions-item>
          
          <el-descriptions-item label="强度等级">
            <el-progress :percentage="(currentExercise.intensity * 100)" 
                         :color="getIntensityColor(currentExercise.intensity)"
                         :stroke-width="20" />
            <span style="margin-left: 10px">{{ (currentExercise.intensity * 100).toFixed(0) }}%</span>
          </el-descriptions-item>
        </el-descriptions>

        <el-divider>训练建议</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="info-box">
              <div class="info-label">推荐时长</div>
              <div class="info-value">{{ currentExercise.recommendedDuration }} 分钟</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-box">
              <div class="info-label">推荐组数</div>
              <div class="info-value">{{ currentExercise.recommendedSets }} 组</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-box">
              <div class="info-label">每组次数</div>
              <div class="info-value">{{ currentExercise.recommendedReps }} 次</div>
            </div>
          </el-col>
        </el-row>

        <el-divider>适应性评分</el-divider>
        
        <div class="suitability-chart">
          <div class="suitability-item">
            <div class="suitability-label">减重效果</div>
            <el-progress :percentage="(currentExercise.suitabilityWeightLoss * 100)" 
                         color="#67c23a" 
                         :stroke-width="15" />
          </div>
          <div class="suitability-item">
            <div class="suitability-label">增肌效果</div>
            <el-progress :percentage="(currentExercise.suitabilityMuscleGain * 100)" 
                         color="#409eff" 
                         :stroke-width="15" />
          </div>
          <div class="suitability-item">
            <div class="suitability-label">耐力提升</div>
            <el-progress :percentage="(currentExercise.suitabilityEndurance * 100)" 
                         color="#e6a23c" 
                         :stroke-width="15" />
          </div>
          <div class="suitability-item">
            <div class="suitability-label">柔韧增强</div>
            <el-progress :percentage="(currentExercise.suitabilityFlexibility * 100)" 
                         color="#f56c6c" 
                         :stroke-width="15" />
          </div>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
        <el-button type="primary" @click="addToTraining">加入训练计划</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { exerciseService, workoutPlanService } from '@/services'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

const exercises = ref([])
const loading = ref(false)
const searchText = ref('')
const detailVisible = ref(false)
const currentExercise = ref(null)
const tableHeight = ref(window.innerHeight - 280)
const authStore = useAuthStore()

const filteredExercises = computed(() => {
  if (!searchText.value) {
    return exercises.value
  }
  const keyword = searchText.value.toLowerCase()
  return exercises.value.filter(exercise => 
    exercise.name.toLowerCase().includes(keyword)
  )
})

const fetchExercises = async () => {
  loading.value = true
  try {
    const res = await exerciseService.getAllExercises()
    if (res.data.code === 200) {
      exercises.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('获取动作列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  // 搜索逻辑已通过computed属性filteredExercises实现
}

const getDifficultyColor = (difficulty) => {
  if (difficulty < 0.3) return '#67c23a'
  if (difficulty < 0.6) return '#e6a23c'
  return '#f56c6c'
}

const getIntensityColor = (intensity) => {
  if (intensity < 0.3) return '#409eff'
  if (intensity < 0.7) return '#e6a23c'
  return '#f56c6c'
}

const getCategoryType = (category) => {
  const types = {
    'CARDIO': 'danger',
    'STRENGTH': 'warning',
    'FLEXIBILITY': 'success',
    'BALANCE': 'info'
  }
  return types[category] || ''
}

const getCategoryName = (category) => {
  const names = {
    'CARDIO': '有氧运动',
    'STRENGTH': '力量训练',
    'FLEXIBILITY': '柔韧训练',
    'BALANCE': '平衡训练'
  }
  return names[category] || category
}

const viewDetail = (exercise) => {
  currentExercise.value = exercise
  detailVisible.value = true
}

const addToTraining = async () => {
  if (!currentExercise.value) return
  try {
    const payload = {
      userId: authStore.user.id,
      exerciseId: currentExercise.value.id,
      sets: currentExercise.value.recommendedSets,
      reps: currentExercise.value.recommendedReps,
      duration: currentExercise.value.recommendedDuration
    }
    const res = await workoutPlanService.addPlanItem(payload)
    if (res.data.code === 200) {
      ElMessage.success('已加入训练计划: ' + currentExercise.value.name)
      detailVisible.value = false
    } else {
      ElMessage.error(res.data.message || '加入训练计划失败')
    }
  } catch (error) {
    ElMessage.error('加入训练计划失败')
  }
}

onMounted(() => {
  fetchExercises()
  window.addEventListener('resize', () => {
    tableHeight.value = window.innerHeight - 280
  })
})
</script>

<style scoped>
.exercises-view {
  width: 100%;
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.exercise-detail {
  padding: 10px;
}

.info-box {
  text-align: center;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 10px;
}

.info-label {
  color: #909399;
  font-size: 14px;
  margin-bottom: 8px;
}

.info-value {
  color: #303133;
  font-size: 24px;
  font-weight: bold;
}

.suitability-chart {
  margin-top: 20px;
}

.suitability-item {
  margin-bottom: 20px;
}

.suitability-label {
  margin-bottom: 8px;
  color: #606266;
  font-weight: 500;
}
</style>
