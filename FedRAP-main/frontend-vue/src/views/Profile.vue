<template>
  <div class="profile-view">
    <el-card>
      <template #header>
        <span>编辑个人资料</span>
      </template>
      
      <el-form :model="profileForm" label-width="120px" v-if="profileForm">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="年龄">
              <el-input-number v-model="profileForm.age" :min="10" :max="100" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别">
              <el-select v-model="profileForm.gender">
                <el-option label="男" value="MALE" />
                <el-option label="女" value="FEMALE" />
                <el-option label="其他" value="OTHER" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="身高 (cm)">
              <el-input-number v-model="profileForm.height" :min="100" :max="250" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="体重 (kg)">
              <el-input-number v-model="profileForm.weight" :min="30" :max="200" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="健身水平">
          <el-slider v-model="fitnessLevel" :min="0" :max="100" :marks="{ 0: '初级', 50: '中级', 100: '高级' }" />
        </el-form-item>

        <el-divider content-position="left">健身目标</el-divider>

        <el-form-item label="减脂">
          <el-slider v-model="goalWeightLoss" :min="0" :max="100" />
        </el-form-item>
        <el-form-item label="增肌">
          <el-slider v-model="goalMuscleGain" :min="0" :max="100" />
        </el-form-item>
        <el-form-item label="耐力">
          <el-slider v-model="goalEndurance" :min="0" :max="100" />
        </el-form-item>
        <el-form-item label="柔韧性">
          <el-slider v-model="goalFlexibility" :min="0" :max="100" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSave" :loading="loading">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { userService } from '@/services'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()
const profileForm = ref(null)
const loading = ref(false)

const fitnessLevel = computed({
  get: () => (profileForm.value?.fitnessLevel || 0) * 100,
  set: (val) => { profileForm.value.fitnessLevel = val / 100 }
})

const goalWeightLoss = computed({
  get: () => (profileForm.value?.goalWeightLoss || 0) * 100,
  set: (val) => { profileForm.value.goalWeightLoss = val / 100 }
})

const goalMuscleGain = computed({
  get: () => (profileForm.value?.goalMuscleGain || 0) * 100,
  set: (val) => { profileForm.value.goalMuscleGain = val / 100 }
})

const goalEndurance = computed({
  get: () => (profileForm.value?.goalEndurance || 0) * 100,
  set: (val) => { profileForm.value.goalEndurance = val / 100 }
})

const goalFlexibility = computed({
  get: () => (profileForm.value?.goalFlexibility || 0) * 100,
  set: (val) => { profileForm.value.goalFlexibility = val / 100 }
})

const fetchProfile = async () => {
  try {
    const res = await userService.getCurrentUser()
    if (res.data.code === 200) {
      profileForm.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('获取资料失败')
  }
}

const handleSave = async () => {
  loading.value = true
  try {
    const res = await userService.updateProfile(authStore.user.id, profileForm.value)
    if (res.data.code === 200) {
      ElMessage.success('保存成功')
      await authStore.fetchCurrentUser()
    }
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.profile-view {
  max-width: 800px;
  margin: 0 auto;
}
</style>
