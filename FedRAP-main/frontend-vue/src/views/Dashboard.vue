<template>
  <el-container class="dashboard-container">
    <el-aside width="250px">
      <div class="logo">
        <h2>个性化健身计划推荐系统</h2>
        <p>智能健身推荐</p>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        router
        background-color="#2c3e50"
        text-color="#ecf0f1"
        active-text-color="#667eea"
      >
        <el-menu-item index="/dashboard/home">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/dashboard/profile">
          <el-icon><User /></el-icon>
          <span>个人中心</span>
        </el-menu-item>
        <el-menu-item index="/dashboard/recommendation">
          <el-icon><MagicStick /></el-icon>
          <span>智能推荐</span>
        </el-menu-item>
        <el-menu-item index="/dashboard/plan">
          <el-icon><List /></el-icon>
          <span>训练计划</span>
        </el-menu-item>
        <el-menu-item index="/dashboard/exercises">
          <el-icon><Trophy /></el-icon>
          <span>动作库</span>
        </el-menu-item>
        <el-menu-item index="/dashboard/training">
          <el-icon><Timer /></el-icon>
          <span>开始训练</span>
        </el-menu-item>
        <el-menu-item index="/dashboard/history">
          <el-icon><Document /></el-icon>
          <span>训练历史</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header>
        <div class="header-content">
          <h3>{{ pageTitle }}</h3>
          <div class="header-right">
            <span>欢迎, {{ authStore.user?.username }}</span>
            <el-button type="danger" size="small" @click="handleLogout">退出</el-button>
          </div>
        </div>
      </el-header>

      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import { House, User, MagicStick, Trophy, Timer, Document, List } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const activeMenu = computed(() => route.path)

const pageTitle = computed(() => {
  const titles = {
    '/dashboard/home': '首页',
    '/dashboard/profile': '个人中心',
    '/dashboard/recommendation': '智能推荐',
    '/dashboard/plan': '训练计划',
    '/dashboard/exercises': '动作库',
    '/dashboard/training': '开始训练',
    '/dashboard/history': '训练历史'
  }
  return titles[route.path] || '个性化健身计划推荐系统'
})

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    authStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }).catch(() => {})
}
</script>

<style scoped>
.dashboard-container {
  height: 100vh;
  background: #f5f7fa;
}

.el-aside {
  background-color: #2c3e50;
  color: #ecf0f1;
}

.logo {
  padding: 30px 20px;
  text-align: center;
  border-bottom: 1px solid #34495e;
}

.logo h2 {
  color: #667eea;
  font-size: 28px;
  margin-bottom: 5px;
}

.logo p {
  color: #95a5a6;
  font-size: 12px;
}

.el-header {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  padding: 0 30px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.header-content h3 {
  color: #2c3e50;
  font-size: 20px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-right span {
  color: #666;
}

.el-main {
  padding: 30px;
  overflow-y: auto;
}
</style>
