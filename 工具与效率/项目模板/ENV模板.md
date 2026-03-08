---
title: "环境变量配置模板"
category: "工具与效率"
tags: ["模板", "环境变量", "配置管理"]
date: 2026-03-02
status: "completed"
---

# .env.example 环境变量模板

> 将此文件复制为项目根目录的 `.env.example`，并根据实际需要修改

---

# 📋 使用说明

1. 复制此文件为 `.env.example`（提交到仓库）
2. 再复制一份为 `.env`（不提交到仓库）
3. 在 `.env` 中填入实际值
4. 在代码中使用环境变量库读取（如 dotenv、viper 等）

---

# 🔧 基础配置

```bash
# 应用环境
NODE_ENV=development

# 应用端口
PORT=3000

# 应用 URL
APP_URL=http://localhost:3000

# API 前缀
API_PREFIX=/api/v1
```

---

# 🔐 认证与密钥

```bash
# JWT 密钥
JWT_SECRET=your-jwt-secret-key-here

# JWT 过期时间
JWT_EXPIRES_IN=7d

# API 密钥（如有外部 API）
API_KEY=your-api-key-here

# 加密密钥
ENCRYPTION_KEY=your-encryption-key-here
```

---

# 🗄️ 数据库配置

```bash
# 数据库类型
DATABASE_TYPE=postgresql

# 数据库连接
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# 或分开配置
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=dbuser
DB_PASSWORD=dbpassword

# Redis 配置（如需要）
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=
```

---

# ☁️ 云服务配置

```bash
# AWS 配置
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=my-bucket-name

# 阿里云配置
ALIYUN_REGION=cn-hangzhou
ALIYUN_ACCESS_KEY_ID=your-access-key
ALIYUN_ACCESS_KEY_SECRET=your-secret-key
ALIYUN_OSS_BUCKET=my-bucket-name

# 腾讯云配置
TENCENT_REGION=ap-guangzhou
TENCENT_SECRET_ID=your-secret-id
TENCENT_SECRET_KEY=your-secret-key
TENCENT_COS_BUCKET=my-bucket-name
```

---

# 📧 邮件服务

```bash
# SMTP 配置
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@yourapp.com

# 或使用邮件服务 API
MAILGUN_API_KEY=your-mailgun-key
MAILGUN_DOMAIN=mg.yourapp.com

SENDGRID_API_KEY=your-sendgrid-key
```

---

# 🔔 通知与监控

```bash
# Sentry 错误追踪
SENTRY_DSN=https://xxx@sentry.io/xxx

# 日志服务
LOG_LEVEL=info
LOG_FORMAT=json

# Slack 通知
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
```

---

# 🔧 第三方服务

```bash
# OpenAI
OPENAI_API_KEY=sk-xxx
OPENAI_ORGANIZATION=org-xxx

# GitHub
GITHUB_TOKEN=ghp_xxx
GITHUB_WEBHOOK_SECRET=webhook-secret

# 支付服务
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# 地图服务
GOOGLE_MAPS_API_KEY=AIzaSy_xxx

# 短信服务
TWILIO_ACCOUNT_SID=ACxxx
TWILIO_AUTH_TOKEN=xxx
```

---

# 🚀 部署配置

```bash
# Docker
DOCKER_REGISTRY=docker.io
DOCKER_IMAGE_NAME=myapp
DOCKER_TAG=latest

# CI/CD
CI_DEPLOY_KEY=xxx
DEPLOY_HOST=deploy.example.com
DEPLOY_USER=deploy
DEPLOY_PATH=/var/www/myapp

# 域名与 SSL
DOMAIN=example.com
SSL_EMAIL=admin@example.com
```

---

# 🧪 测试环境

```bash
# 测试数据库
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/testdb

# 测试用密钥
TEST_STRIPE_KEY=sk_test_xxx
TEST_API_KEY=test-key-xxx

# Mock 外部服务
MOCK_EXTERNAL_API=true
```

---

# 📁 文件存储

```bash
# 上传目录
UPLOAD_DIR=./uploads

# 最大文件大小 (MB)
MAX_FILE_SIZE=10

# 允许的文件类型
ALLOWED_FILE_TYPES=jpg,jpeg,png,gif,pdf

# 或使用云存储
STORAGE_TYPE=s3  # local/s3/oss/cos
S3_UPLOAD_BUCKET=myapp-uploads
```

---

# 🔒 安全配置

```bash
# CORS 允许的域名
CORS_ORIGIN=http://localhost:3000,https://example.com

# 速率限制
RATE_LIMIT_WINDOW=15  # 分钟
RATE_LIMIT_MAX=100    # 次数

# 会话配置
SESSION_SECRET=your-session-secret
SESSION_MAX_AGE=86400000  # 毫秒
```

---

# 📊 特性开关

```bash
# 功能开关
FEATURE_NEW_UI=false
FEATURE_BETA_API=true
FEATURE_MAINTENANCE=false

# 调试模式
DEBUG=false
VERBOSE_LOGGING=false
```

---

# ⚠️ 重要提示

1. **永远不要提交 `.env` 文件到 Git 仓库**
2. 确保 `.env` 在 `.gitignore` 中
3. 使用 `.env.example` 说明需要哪些环境变量
4. 生产环境使用专业的密钥管理服务（如 AWS Secrets Manager）
5. 定期轮换敏感密钥

---

*模板版本: 1.0.0 | 最后更新: 2026-03-02*
