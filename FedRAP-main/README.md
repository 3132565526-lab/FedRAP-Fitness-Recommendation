# 基于联邦学习的个性化健身计划推荐系统 (FedRAP Fitness)

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Java](https://img.shields.io/badge/Java-17-orange.svg)
![Vue](https://img.shields.io/badge/Vue.js-3.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.2.0-brightgreen.svg)

本项目是一个基于**联邦学习 (Federated Learning)** 思想架构的个性化健身计划推荐系统。项目采用前后端分离架构，结合轻量级的联邦推荐算法 (FedRAP)，在保护用户隐私数据的前提下，实现了智能、动态的健身体验。

## 🌟 核心功能

- **用户系统**：安全的JWT鉴权，详细的身体画像管理（身高、体重、BMI计算、健身目标动态跟踪）。
- **智能推荐引擎**：
  - **初级阶段（冷启动）**：使用内置的规则引擎，根据用户的初步选项进行基础推荐。
  - **高级阶段（联邦推荐）**：自动调用本地基于 PyTorch 训练的联邦推荐模型（FedRAP）进行高度个性化的健身动作预测，无需上传敏感生理数据。，
- **计划与历史管理**：动作计划自动动态调整；完成动作后智能移除并保存到历史记录中。
- **动作资源库**：涵盖力量、有氧、柔韧等各维度的动作库浏览功能。

---

## 🛠️ 技术栈说明

| 领域 | 技术 / 框架 | 描述 |
| :--- | :--- | :--- |
| **前端 (Frontend)** | Vue 3 + Vite + Element Plus + Pinia | 响应式界面开发与全局状态管理 |
| **后端 (Backend)** | Java 17 + Spring Boot 3.2.0 + Spring Security | RESTful接口，业务逻辑与安全控制 |
| **数据库 (Database)** | H2 Database (内嵌) | 轻量化本地存储，**免安装无配置**，开箱即用（支持一键切换MySQL） |
| **算法端 (ML/AI)** | Python 3.8+ / PyTorch 2.x | 负责FedRAP模型推理（`model_inference.py`）及数据处理 |

---

## 🚀 本地快速运行指南 (Installation & Setup)

为了确保您能顺利运行本项目，请确保您的计算机上已安装以下环境：
1. **[JDK 17+](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)** （必须为17及以上）
2. **[Node.js 16+](https://nodejs.org/)** （推荐 LTS 版本）
3. **[Python 3.8+](https://www.python.org/downloads/)** （用于模型推理）

### 第1步：克隆项目

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 第2步：配置算法推理环境 (Python)

由于Java后端会拉起本地Python模型进行推荐计算，需要先配置AI环境：

```bash
# 建议使用虚拟环境（以 venv 为例）
python -m venv .venv

# 激活虚拟环境 (Windows)
.venv\Scripts\activate
# 激活虚拟环境 (Mac/Linux)
# source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 第3步：启动后端服务 (Java Spring Boot)

后端使用内嵌的 H2 数据库，**不需要手动安装和配置 MySQL**，数据文件会自动生成在 `backend-java/data/fedrapdb` 下。

**方式 A：使用预置脚本（仅限 Windows）**
直接双击项目根目录下的 `启动后端-Java.bat`。

**方式 B：使用命令启动**
```bash
# 进入后端目录
cd backend-java

# 使用 Maven 运行（如果没有安装外部 Maven，可以使用项目中自带的 mvnw 包装器）
mvn spring-boot:run
# 或者 Windows 下使用:
# mvnw.cmd spring-boot:run
```
后端成功启动后，服务将运行在 `http://localhost:8080/api`。

### 第4步：启动前端项目 (Vue 3)

**方式 A：使用预置脚本（仅限 Windows）**
直接双击项目根目录下的 `启动前端-Vue.bat`（初次运行脚本会自动执行 npm install 安装依赖）。

**方式 B：使用命令启动**
```bash
# 进入前端目录
cd frontend-vue

# 初次运行需要安装依赖包
npm install

# 启动 Vite 开发服务器
npm run dev
```
前端成功启动后，在浏览器访问 `http://localhost:5173` 即可进入系统。

---

## 📂 项目结构概览

```text
FedRAP-main/
  ├── backend-java/                # Java Spring Boot 核心后端（含 H2 配置文件）
  ├── frontend-vue/                # Vue 3 前端界面源码
  ├── model/                       # 联邦学习训练算法相关代码
  ├── datasets/fitness/            # 数据集，用于冷启动或重新生成特征
  ├── results/checkpoints/         # 本地已训练完成的模型权重(.[best]EpochX.model)
  ├── 启动后端-Java.bat            # Windows 快捷启动脚本
  ├── 启动前端-Vue.bat             # Windows 快捷启动脚本
  ├── requirements.txt             # Python 运行库依赖表
  └── model_inference.py           # Java调用的Python推理脚本入口
```

## ❓ 常见问题排查 (FAQ)

1. **Python script failed (模型推荐报错)**
   - 检查 `java` 运行环境中 `python` 命令是否指向刚才配置了依赖的 Python 目录（推荐设置全局环境变量，或在IDEA等开发工具中直接将全局Python设置好）。
   - 检查是否缺少 `requirements.txt` 中的包，尤其是 `torch` 或 `pandas`。
   
2. **端口占用错误 (Port Already in Use)**
   - 后端默认 `8080`，前端默认 `5173`。
   - 若被占用，前端在 `vite.config.js` 修改，后端在 `application.yml` 配置 `server.port` 修改；修改后务必同步前端 `api.js` 中调用的 Base URL。

3. **数据重置**
   - 如果想清除所有 H2 数据库文件，只需删除 `backend-java/data/` 目录中的 `fedrapdb.mv.db` 文件，重启后端后将自动重建结构。

## 📄 许可证

基于 [MIT License](LICENSE) 协议开源，欢迎学习交流。
