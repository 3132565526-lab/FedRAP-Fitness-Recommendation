<template>
  <div class="history-view">
    <el-card>
      <template #header>
        <span>训练历史</span>
      </template>

      <el-timeline v-loading="loading">
        <el-timeline-item
          v-for="record in history"
          :key="record.id"
          :timestamp="formatDate(record.trainingDate)"
          placement="top"
        >
          <el-card>
            <h4>{{ record.exercise?.name }}</h4>
            <p>时长: {{ record.duration }} 分钟 | 组数: {{ record.sets }} | 次数: {{ record.reps }}</p>
            <p v-if="record.caloriesBurned">消耗: {{ record.caloriesBurned }} kcal</p>
            <el-rate v-model="record.rating" disabled />
          </el-card>
        </el-timeline-item>
      </el-timeline>

      <el-empty v-if="!loading && history.length === 0" description="还没有训练记录" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { trainingService } from '@/services'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()
const history = ref([])
const loading = ref(false)

const fetchHistory = async () => {
  loading.value = true
  try {
    const res = await trainingService.getTrainingHistory(authStore.user.id)
    if (res.data.code === 200) {
      history.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('获取训练历史失败')
  } finally {
    loading.value = false
  }
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchHistory()
})
</script>

<style scoped>
.history-view {
  max-width: 1000px;
  margin: 0 auto;
}
</style>
