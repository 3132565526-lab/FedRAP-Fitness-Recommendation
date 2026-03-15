<template>
  <div class="plan-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>个人训练计划</span>
          <div class="header-actions">
            <el-button size="small" @click="fetchPlan" :loading="loading">刷新</el-button>
            <el-button size="small" type="primary" @click="$router.push('/dashboard/recommendation')">
              去智能推荐
            </el-button>
            <el-button size="small" @click="$router.push('/dashboard/exercises')">
              去动作库
            </el-button>
          </div>
        </div>
      </template>

      <div v-if="!loading && !plan">
        <el-empty description="还没有个人训练计划">
          <template #extra>
            <el-button type="primary" @click="$router.push('/dashboard/recommendation')">
              从推荐添加
            </el-button>
          </template>
        </el-empty>
      </div>

      <div v-else>
        <div class="plan-meta">
          <div>
            <strong>{{ plan?.planName || '个人训练计划' }}</strong>
            <span class="plan-desc">{{ plan?.description || '个人自选训练计划' }}</span>
          </div>
          <div class="plan-stats">
            <span>总时长：{{ plan?.totalDuration || 0 }} 分钟</span>
            <span>预估消耗：{{ plan?.estimatedCalories || 0 }} kcal</span>
          </div>
        </div>

        <el-table
          :data="plan?.exercises || []"
          v-loading="loading"
          stripe
          style="width: 100%"
        >
          <el-table-column prop="orderIndex" label="序号" width="80" align="center" />
          <el-table-column prop="exerciseName" label="动作名称" min-width="200" />
          <el-table-column prop="sets" label="组数" width="100" align="center" />
          <el-table-column prop="reps" label="次数" width="100" align="center" />
          <el-table-column prop="duration" label="时长(分钟)" width="120" align="center" />
          <el-table-column label="操作" width="200" align="center">
            <template #default="{ row }">
              <el-button size="small" type="primary" @click="startTraining(row)">开始训练</el-button>
              <el-button size="small" type="danger" @click="removeItem(row)">移除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-empty
          v-if="!loading && (plan?.exercises || []).length === 0"
          description="训练计划为空"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { workoutPlanService } from '@/services'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

const plan = ref(null)
const loading = ref(false)

const fetchPlan = async () => {
  loading.value = true
  try {
    const res = await workoutPlanService.getActivePlan(authStore.user.id)
    if (res.data.code === 200) {
      plan.value = res.data.data
    } else {
      ElMessage.error(res.data.message || '获取训练计划失败')
    }
  } catch (error) {
    ElMessage.error('获取训练计划失败')
  } finally {
    loading.value = false
  }
}

const startTraining = (item) => {
  router.push({
    path: '/dashboard/training',
    query: { exerciseId: item.exerciseId }
  })
}

const removeItem = (item) => {
  if (!plan.value) return
  ElMessageBox.confirm('确定要移除该动作吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      const res = await workoutPlanService.removePlanItem(
        plan.value.id,
        item.exerciseId,
        authStore.user.id
      )
      if (res.data.code === 200) {
        plan.value = res.data.data
        ElMessage.success('已移除')
      } else {
        ElMessage.error(res.data.message || '移除失败')
      }
    } catch (error) {
      ElMessage.error('移除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchPlan()
})
</script>

<style scoped>
.plan-view {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.plan-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0 20px;
  gap: 12px;
}

.plan-desc {
  margin-left: 12px;
  color: #666;
  font-size: 12px;
}

.plan-stats {
  display: flex;
  gap: 16px;
  color: #666;
}
</style>
