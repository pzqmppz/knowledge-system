**域名邮箱配置指南**

dolosy.cn 自定义邮箱 · Cloudflare Email Routing + Gmail

方案概述

使用 Cloudflare Email Routing 接收邮件，Gmail SMTP
发送邮件，实现完全免费的自定义域名邮箱。

- 收信：发到 wehan@dolosy.cn 的邮件自动转发至 Gmail

- 发信：在 Gmail 中以 wehan@dolosy.cn 身份发件

- 费用：完全免费

第一步：迁移 DNS 到 Cloudflare

**注意：**A 记录全部设为灰色云朵（仅DNS模式），确保网站流量不经过
Cloudflare 代理，避免国内访问变慢。

1.  注册 cloudflare.com，添加域名 dolosy.cn

2.  Cloudflare 扫描并导入现有 DNS 记录（4条 A 记录）

3.  将 4 条 A 记录的橙色云朵点为灰色（仅DNS）

4.  前往腾讯云域名控制台 → dolosy.cn 管理 → 基本信息 → 修改 DNS 服务器

- cheryl.ns.cloudflare.com

- jakub.ns.cloudflare.com

5.  等待 DNS 生效（几分钟至48小时）

第二步：配置 Cloudflare Email Routing（收信）

6.  Cloudflare 控制台 → dolosy.cn → Email → Email Routing

7.  点击 Get Started，填写自定义地址前缀（如 wehan）及目标 Gmail 地址

8.  Cloudflare 自动添加 MX 和 SPF 记录（点击自动添加）

9.  前往 Gmail 收取验证邮件并点击确认链接

第三步：配置 Gmail 发信（显示自定义域名）

3.1 获取 Gmail 应用专用密码

10. Google 账号 → 安全性 → 开启两步验证

11. 搜索\"应用专用密码\" -\> 创建并保存生成的密码

3.2 在 Gmail 添加发信地址

12. Gmail → 设置 → 查看所有设置 → 账号和导入

13. 「以以下地址发送邮件」→ 添加其他电子邮件地址

14. 填写 wehan@dolosy.cn，取消勾选【视为别名】

15. SMTP 配置：

- SMTP 服务器：smtp.gmail.com

- 端口：587

- 用户名：你的完整 Gmail 地址

- 密码：第 3.1 步生成的应用专用密码

16. 前往 Gmail 收取验证邮件并点击确认链接

验证测试

- **收信测试：**用其他邮箱发送邮件至 wehan@dolosy.cn，Gmail 应能收到

- **发信测试：**Gmail 写新邮件 → 发件人下拉选择 wehan@dolosy.cn 发送

注意事项

- DNS 切换到 Cloudflare 后，新增域名解析均需在 Cloudflare 控制台操作

- 网站 A 记录保持灰色（仅DNS），不影响国内访问速度

- 邮件路由与服务器无关，不影响上海服务器的正常运行

- 备案不受影响，备案管理的是网站内容，与 DNS 服务商无关
