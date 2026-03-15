# FedRAP 智能健身推荐系统 - Java + Vue 版本

## 项目简介

这是一个基于 **Java Spring Boot** 后端 + **Vue 3** 前端的智能健身计划推荐平台，采用联邦学习思想实现个性化推荐。

### 技术栈

**后端 (Backend)**
- Java 17
- Spring Boot 3.2.0
- Spring Security + JWT
- Spring Data JPA
- H2 Database (可切换为 MySQL)
- Maven

**前端 (Frontend)**
- Vue 3
- Vite
- Vue Router
- Pinia (状态管理)
- Element Plus (UI 组件库)
- Axios
- Chart.js

## 项目结构

```
FedRAP-main/
├── backend-java/              # Java 后端项目
│   ├── src/
│   │   └── main/
│   │       ├── java/com/fedrap/fitness/
│   │       │   ├── FitnessRecommendationApplication.java
│   │       │   ├── controller/      # REST API 控制器
│   │       │   ├── service/         # 业务逻辑层
│   │       │   ├── model/           # 实体和 DTO
│   │       │   ├── repository/      # 数据访问层
│   │       │   ├── security/        # JWT 认证
│   │       │   └── config/          # 配置类
│   │       └── resources/
│   │           └── application.yml  # 应用配置
│   └── pom.xml                      # Maven 配置
│
├── frontend-vue/             # Vue 前端项目
│   ├── src/
│   │   ├── views/           # 页面组件
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── services/        # API 服务
│   │   ├── router/          # 路由配置
│   │   ├── App.vue          # 根组件
│   │   └── main.js          # 入口文件
│   ├── index.html
│   ├── vite.config.js       # Vite 配置
│   └── package.json         # NPM 配置
│
├── 启动后端.bat              # 后端启动脚本
├── 启动前端.bat              # 前端启动脚本
└── README-Java-Vue.md       # 本文档
```

## 快速开始

### 环境要求

1. **Java 环境**
   - JDK 17 或更高版本
   - Maven 3.6+

2. **Node.js 环境**
   - Node.js 16+ 
   - npm 或 yarn

### 安装步骤

#### 1. 启动后端

**方法一：使用启动脚本（推荐）**
```bash
# Windows
启动后端.bat
```

**方法二：手动启动**
```bash
cd backend-java
mvn spring-boot:run
```

后端将在 `http://localhost:8080/api` 启动

#### 2. 启动前端

**方法一：使用启动脚本（推荐）**
```bash
# Windows
启动前端.bat
```

**方法二：手动启动**
```bash
cd frontend-vue

# 首次运行需要安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 `http://localhost:5173` 启动

### 3. 访问系统

打开浏览器访问: `http://localhost:5173`

- 首次使用请先注册账号
- 注册后自动登录进入系统

## 核心功能

### 1. 用户认证
- 用户注册/登录
- JWT Token 认证
- 安全的密码加密

### 2. 个人中心
- 个人信息管理（年龄、身高、体重、BMI）
- 健身水平设置
- 健身目标配置（减脂/增肌/耐力/柔韧性）
- 身体维度记录

### 3. 智能推荐
- 基于用户画像的个性化推荐
- 综合考虑：
  - 用户健身目标匹配度
  - 难度适配度
  - 训练历史偏好
  - 多样性均衡

### 4. 动作库
- 完整的健身动作数据库
- 动作分类（力量/有氧/柔韧/平衡）
- 动作详情查看

### 5. 训练记录
- 训练历史记录
- 训练数据统计
- 经验值和等级系统

## API 接口说明

### 认证接口
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录

### 用户接口
- `GET /api/users/me` - 获取当前用户信息
- `GET /api/users/{userId}` - 获取用户信息
- `PUT /api/users/{userId}` - 更新用户资料

### 推荐接口
- `POST /api/recommendations` - 获取推荐
- `GET /api/recommendations/user/{userId}` - 获取用户推荐

### 动作接口
- `GET /api/exercises/list` - 获取所有动作
- `GET /api/exercises/{exerciseId}` - 获取动作详情
- `GET /api/exercises/category/{category}` - 按类别获取动作

### 训练接口
- `POST /api/training/record` - 记录训练
- `GET /api/training/history/{userId}` - 获取训练历史
- `GET /api/training/stats/{userId}` - 获取训练统计

## 数据库配置

### 使用 H2 内存数据库（默认）

无需额外配置，数据存储在内存中，重启后数据丢失。

访问 H2 控制台: `http://localhost:8080/api/h2-console`
- JDBC URL: `jdbc:h2:mem:fitnessdb`
- Username: `sa`
- Password: (留空)

### 切换到 MySQL

1. 编辑 `backend-java/src/main/resources/application.yml`

2. 注释掉 H2 配置，启用 MySQL 配置：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/fitness_db?useSSL=false&serverTimezone=UTC&characterEncoding=utf8
    driver-class-name: com.mysql.cj.jdbc.Driver
    username: root
    password: your_password
  
  jpa:
    hibernate:
      ddl-auto: update
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQLDialect
```

3. 创建数据库：
```sql
CREATE DATABASE fitness_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 开发说明

### 后端开发

1. **添加新的 API 接口**
   - 在 `controller` 包中创建或修改控制器
   - 在 `service` 包中实现业务逻辑
   - 在 `repository` 包中定义数据访问接口

2. **添加新的数据模型**
   - 在 `model.entity` 包中创建实体类
   - 在 `model.dto` 包中创建 DTO 类

3. **配置修改**
   - 编辑 `application.yml` 文件

### 前端开发

1. **添加新页面**
   - 在 `src/views/` 创建 Vue 组件
   - 在 `src/router/index.js` 添加路由

2. **添加新的 API 服务**
   - 在 `src/services/index.js` 添加服务函数

3. **状态管理**
   - 在 `src/stores/` 创建 Pinia store

## 生产部署

### 后端部署

```bash
cd backend-java
mvn clean package
java -jar target/fitness-recommendation-1.0.0.jar
```

### 前端部署

```bash
cd frontend-vue
npm run build
# 将 dist 目录部署到 Web 服务器
```

## 常见问题

### 1. 端口占用
- 后端默认端口: 8080
- 前端默认端口: 5173
- 如需修改，请编辑对应的配置文件

### 2. 跨域问题
- 后端已配置 CORS 支持
- 前端已配置代理转发

### 3. JWT Token 过期
- 默认有效期: 7 天
- 可在 `application.yml` 中修改

## 系统架构

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Vue 3     │ ◄─────► │  Spring Boot │ ◄─────► │  Database   │
│  Frontend   │  HTTP   │    Backend   │  JPA    │  (H2/MySQL) │
│ (Port 5173) │  REST   │  (Port 8080) │         │             │
└─────────────┘         └──────────────┘         └─────────────┘
      │                        │
      │                        │
   Element Plus          Spring Security
   Vue Router                 JWT
   Pinia                   Hibernate
   Axios
```

## 许可证

MIT License

## 联系方式

如有问题，请提交 Issue 或联系开发团队。

---

**开发团队**: FedRAP Team  
**版本**: 1.0.0  
**更新日期**: 2026-01-26
