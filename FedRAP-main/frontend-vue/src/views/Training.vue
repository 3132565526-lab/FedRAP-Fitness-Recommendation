<template>
  <div class="training-view">
    <el-card>
      <template #header>
        <span>开始训练</span>
      </template>

      <div v-if="!exerciseId">
        <el-result icon="success" title="训练功能" sub-title="请在推荐页面选择动作开始训练">
          <template #extra>
            <el-button type="primary" @click="$router.push('/dashboard/recommendation')">
              前往推荐
            </el-button>
          </template>
        </el-result>
      </div>

      <div v-else>
        <el-skeleton :loading="loading" animated>
          <template #default>
            <div class="exercise-info">
              <h3>{{ exercise?.name }}</h3>
              <p class="desc">{{ exercise?.description }}</p>
              <div class="meta">
                <span>类别：{{ exercise?.category }}</span>
                <span>目标肌群：{{ exercise?.targetMuscle }}</span>
                <span>器械：{{ exercise?.equipment }}</span>
              </div>
            </div>

            <el-divider />

            <el-form :model="form" label-width="120px" class="training-form">
              <el-form-item label="训练时长(分钟)">
                <el-input-number v-model="form.duration" :min="5" :max="180" />
              </el-form-item>
              <el-form-item label="组数">
                <el-input-number v-model="form.sets" :min="1" :max="20" />
              </el-form-item>
              <el-form-item label="每组次数">
                <el-input-number v-model="form.reps" :min="1" :max="200" />
              </el-form-item>
              <el-form-item label="重量(kg)">
                <el-input-number v-model="form.weight" :min="0" :max="500" :precision="1" />
              </el-form-item>
              <el-form-item label="消耗卡路里">
                <el-input-number v-model="form.caloriesBurned" :min="0" :max="3000" />
              </el-form-item>
              <el-form-item label="平均心率">
                <el-input-number v-model="form.heartRateAvg" :min="40" :max="220" />
              </el-form-item>
              <el-form-item label="最大心率">
                <el-input-number v-model="form.heartRateMax" :min="40" :max="220" />
              </el-form-item>
              <el-form-item label="疲劳程度">
                <el-slider v-model="form.fatigueLevel" :min="0" :max="1" :step="0.1" show-input />
              </el-form-item>
              <el-form-item label="难度反馈">
                <el-slider v-model="form.difficultyFeedback" :min="0" :max="1" :step="0.1" show-input />
              </el-form-item>
              <el-form-item label="训练评分">
                <el-rate v-model="form.rating" />
              </el-form-item>
              <el-form-item label="备注">
                <el-input v-model="form.notes" type="textarea" :rows="3" placeholder="记录你的训练感受" />
              </el-form-item>

              <el-form-item>
                <el-button type="primary" :loading="submitting" @click="submitTraining">
                  提交训练记录
                </el-button>
                <el-button @click="resetForm">重置</el-button>
              </el-form-item>
            </el-form>
          </template>
        </el-skeleton>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { exerciseService, trainingService } from '@/services'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const submitting = ref(false)
const exercise = ref(null)

const exerciseId = computed(() => {
  const id = Number(route.query.exerciseId)
  return Number.isFinite(id) && id > 0 ? id : null
})

const form = ref({
  duration: 20,
  sets: 3,
  reps: 12,
  weight: 0,
  rating: 4,
  fatigueLevel: 0.5,
  difficultyFeedback: 0.5,
  notes: '',
  caloriesBurned: 0,
  heartRateAvg: 120,
  heartRateMax: 150
})

const applyDefaultsFromExercise = () => {
  if (!exercise.value) return
  form.value.duration = exercise.value.recommendedDuration || form.value.duration
  form.value.sets = exercise.value.recommendedSets || form.value.sets
  form.value.reps = exercise.value.recommendedReps || form.value.reps
  const perMinute = exercise.value.caloriesPerMinute || 0
  form.value.caloriesBurned = Math.round(perMinute * (form.value.duration || 0))
}

const fetchExercise = async () => {
  if (!exerciseId.value) return
  loading.value = true
  try {
    const res = await exerciseService.getExerciseById(exerciseId.value)
    if (res.data.code === 200) {
      exercise.value = res.data.data
      applyDefaultsFromExercise()
    } else {
      ElMessage.error('获取动作信息失败')
    }
  } catch (error) {
    ElMessage.error('获取动作信息失败')
  } finally {
    loading.value = false
  }
}

const submitTraining = async () => {
  if (!exerciseId.value) {
    ElMessage.warning('请先从推荐页面选择动作')
    return
  }
  submitting.value = true
  try {
    const payload = {
      userId: authStore.user.id,
      exerciseId: exerciseId.value,
      duration: form.value.duration,
      sets: form.value.sets,
      reps: form.value.reps,
      weight: form.value.weight,
      rating: form.value.rating,
      fatigueLevel: form.value.fatigueLevel,
      difficultyFeedback: form.value.difficultyFeedback,
      notes: form.value.notes,
      caloriesBurned: form.value.caloriesBurned,
      heartRateAvg: form.value.heartRateAvg,
      heartRateMax: form.value.heartRateMax
    }
    const res = await trainingService.recordTraining(payload)
    if (res.data.code === 200) {
      ElMessage.success('训练记录已保存')
      router.push('/dashboard/history')
    } else {
      ElMessage.error(res.data.message || '保存失败')
    }
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  form.value = {
    duration: 20,
    sets: 3,
    reps: 12,
    weight: 0,
    rating: 4,
    fatigueLevel: 0.5,
    difficultyFeedback: 0.5,
    notes: '',
    caloriesBurned: 0,
    heartRateAvg: 120,
    heartRateMax: 150
  }
  applyDefaultsFromExercise()
}

watch(
  () => form.value.duration,
  (val) => {
    const perMinute = exercise.value?.caloriesPerMinute || 0
    form.value.caloriesBurned = Math.round(perMinute * (val || 0))
  }
)

onMounted(() => {
  fetchExercise()
})
</script>

<style scoped>
.training-view {
  max-width: 800px;
  margin: 0 auto;
}

.exercise-info h3 {
  margin: 0 0 6px 0;
  font-size: 20px;
}

.desc {
  color: #666;
  margin-bottom: 8px;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  color: #888;
  font-size: 13px;
}

.training-form {
  margin-top: 10px;
}
</style>
