# Dify 本地部署指南

> Dify 是一个开源的 LLM 应用开发平台，支持可视化编排工作流、Agent、知识库等功能
>
> 部署日期：2026-03-06
>
> 访问地址：http://localhost:8090

---

## 🚀 快速开始 - 常用命令

### 服务管理

```bash
# 进入 Dify 目录
cd "E:\ai-deploy\dify\docker"

# 查看服务状态
docker compose ps

# 查看所有容器状态（含健康检查）
docker compose ps -a

# 查看实时日志
docker compose logs -f

# 查看特定服务日志
docker compose logs -f api
docker compose logs -f nginx
docker compose logs -f worker

# 停止所有服务
docker compose down

# 停止并删除数据卷（⚠️ 会清空数据）
docker compose down -v

# 启动所有服务
docker compose up -d

# 重启特定服务
docker compose restart api
docker compose restart nginx
```

### 故障排查

```bash
# 查看服务资源占用
docker stats

# 进入容器内部
docker exec -it docker-api-1 bash
docker exec -it docker-db_postgres-1 psql -U postgres

# 检查网络连接
docker network inspect docker_default

# 查看容器详细信息
docker inspect docker-api-1
```

### 数据备份

```bash
# 备份数据库
docker exec docker-db_postgres-1 pg_dump -U postgres dify > backup.sql

# 恢复数据库
docker exec -i docker-db_postgres-1 psql -U postgres dify < backup.sql

# 备份整个数据目录
cp -r "E:\ai-deploy\dify\docker\volumes" "E:\backup\dify-$(date +%Y%m%d)"
```

---

## 📖 Dify 简介

### 什么是 Dify？

Dify 是一个开源的 LLM 应用开发平台，提供以下核心功能：

| 功能 | 说明 |
|------|------|
| **可视化编排** | 拖拽式构建 AI 应用，无需编码 |
| **Agent** | 创建自主智能体，支持工具调用 |
| **工作流** | 复杂任务的多步骤自动化处理 |
| **知识库** | 上传文档，构建 RAG 应用 |
| **模型支持** | 接入 OpenAI、Ollama、LocalAI 等 |
| **API 服务** | 将应用发布为 API 接口 |

### Dify vs Coze vs n8n

| 维度 | Dify | Coze 开源版 | n8n |
|------|------|------------|------|
| **维护状态** | ✅ 活跃 | ❌ 停滞 | ✅ 活跃 |
| **学习曲线** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **本地模型支持** | ✅ 原生支持 | ⚠️ 复杂 | ⚠️ 需配置 |
| **知识库功能** | ✅ 强大 | ✅ 有 | ❌ 无 |
| **工作流能力** | ✅ 强大 | ✅ 强大 | ✅ 最强 |
| **适用场景** | AI 应用开发 | 快速原型 | 通用自动化 |

---

## 📦 部署信息

### 部署环境

| 项目 | 值 |
|------|------|
| **部署目录** | `E:\ai-deploy\dify\docker` |
| **配置文件** | `E:\ai-deploy\dify\docker\.env` |
| **数据目录** | `E:\ai-deploy\dify\docker\volumes` |
| **Web 端口** | 8090 |
| **API 端口** | 8090 (通过 Nginx) |
| **Docker 网络** | docker_default |

### 服务列表

| 容器名 | 服务 | 端口 | 说明 |
|--------|------|------|------|
| docker-nginx-1 | Nginx | 8090, 443 | 反向代理 |
| docker-api-1 | API | 5001 | 后端服务 |
| docker-web-1 | Web | 3000 | 前端界面 |
| docker-db_postgres-1 | PostgreSQL | 5432 | 数据库 |
| docker-redis-1 | Redis | 6379 | 缓存 |
| docker-weaviate-1 | Weaviate | - | 向量数据库 |
| docker-worker-1 | Worker | - | 任务队列 |
| docker-worker_beat-1 | Worker Beat | - | 定时任务 |
| docker-sandbox-1 | Sandbox | - | 代码沙箱 |
| docker-plugin_daemon-1 | Plugin Daemon | 5003 | 插件服务 |
| docker-ssrf_proxy-1 | SSRF Proxy | 3128 | 安全代理 |

---

## 🌐 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| **控制台** | http://localhost:8090/console | 管理界面 |
| **应用市场** | http://localhost:8090 | 应用访问 |
| **API 文档** | http://localhost:8090/docs | API 文档 |

---

## 🔧 配置说明

### 已修改配置

`.env` 文件中修改了以下配置：

```bash
# 端口配置（避免与 n8n 的 8080 冲突）
NGINX_PORT=8090
EXPOSE_NGINX_PORT=8090
```

### 重要配置项

```bash
# 日志级别
LOG_LEVEL=INFO

# 数据库
DB_USERNAME=postgres
DB_PASSWORD=difyai123456
DB_HOST=db_postgres
DB_PORT=5432
DB_DATABASE=dify

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# 向量数据库
VECTOR_STORE=weaviate
```

---

## 📚 部署步骤回顾

### 1. 克隆仓库

```bash
cd "E:\ai-deploy"
git clone https://github.com/langgenius/dify.git
```

### 2. 复制配置文件

```bash
cd "E:\ai-deploy\dify\docker"
cp .env.example .env
```

### 3. 修改端口配置

```bash
sed -i 's/^NGINX_PORT=80$/NGINX_PORT=8090/' .env
sed -i 's/^EXPOSE_NGINX_PORT=80$/EXPOSE_NGINX_PORT=8090/' .env
```

### 4. 启动服务

```bash
docker compose up -d
```

### 5. 等待启动完成

启动需要 3-5 分钟，等待所有服务变为 `Up (healthy)` 状态。

---

## ⚠️ 常见问题

### Q1: 端口被占用

**错误**: `Bind for 0.0.0.0:8090 failed: port is already allocated`

**解决**:
```bash
# 查看占用端口的进程
netstat -ano | findstr :8090

# 修改 .env 文件中的端口
NGINX_PORT=8091
EXPOSE_NGINX_PORT=8091

# 重启服务
docker compose down
docker compose up -d
```

### Q2: 服务启动失败

**排查步骤**:
```bash
# 1. 查看服务状态
docker compose ps

# 2. 查看日志
docker compose logs

# 3. 检查磁盘空间
df -h

# 4. 重启服务
docker compose restart
```

### Q3: 数据丢失

**预防**:
- 定期备份 `volumes` 目录
- 使用数据库备份命令
- 不要轻易使用 `docker compose down -v`

### Q4: 内存不足

**现象**: 服务频繁重启

**解决**:
- 停止不用的 Docker 容器
- 增加 Docker 资源限制
- 减少并发 worker 数量

---

## 🎯 下一步

### 首次使用

1. 打开 http://localhost:8090
2. 注册管理员账号
3. 创建第一个应用

### 接入本地模型

Dify 支持通过 OpenAI 兼容 API 接入本地模型：

**Ollama**:
```
模型提供商: OpenAI Compatible
API Base URL: http://host.docker.internal:11434/v1
API Key: sk-xxx (任意填写)
```

**LocalAI**:
```
模型提供商: OpenAI Compatible
API Base URL: http://host.docker.internal:8080/v1
API Key: sk-xxx (任意填写)
```

### 学习资源

- 官方文档: https://docs.dify.ai
- GitHub: https://github.com/langgenius/dify
- 社区: https://discord.gg/dify

---

## 📝 版本信息

| 项目 | 版本 |
|------|------|
| Dify | 1.13.0 |
| PostgreSQL | 15-alpine |
| Redis | 6-alpine |
| Weaviate | 1.27.0 |
| Nginx | latest |

---

*文档版本: 1.0*
*创建日期: 2026-03-06*
*相关文档：[本地大模型公网暴露方案.md](./本地大模型公网暴露方案.md) | [n8n 学习笔记](./n8n学习笔记.md)*
