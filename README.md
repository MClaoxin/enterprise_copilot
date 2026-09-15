# Enterprise Copilot

Enterprise Copilot 的 Week 2 可展示版本：一个基于 FastAPI、SQLAlchemy 和
PostgreSQL 的多租户业务 API。目前提供健康检查、用户与工作区接口，并具备统一异常响应、
JSON 日志、请求 ID 和持续集成检查。

## 快速开始

前置要求：Python 3.10+、[uv](https://docs.astral.sh/uv/)；连接持久化接口时还需要
PostgreSQL。复制环境变量模板并按本地环境填写：

```powershell
Copy-Item apps/api/.env.example apps/api/.env
Set-Location apps/api
uv sync --locked --dev
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

服务启动后可访问：

- OpenAPI 文档：<http://localhost:8000/docs>
- 健康检查：<http://localhost:8000/health>
- 用户 API：`/api/v1/users`
- 工作区 API：`/api/v1/workspaces`
- 认证 API：`/api/v1/auth/register`、`/login`、`/refresh`、`/me`

也可以从仓库根目录启动完整基础设施：

```powershell
docker compose up --build
```

## API 示例

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com","password":"secure-password"}'
```

认证使用 Argon2 存储密码哈希。Access Token 默认有效 15 分钟，Refresh Token 默认
有效 7 天，两者通过 JWT 的 `type` 声明隔离。访问 Workspace 接口需要 Bearer Token；
角色权限按 `viewer < member < admin < owner` 递增。生产环境的 `JWT_SECRET_KEY`
应使用至少 32 字节的随机密钥。

错误响应采用统一格式，`request_id` 同时写入 `X-Request-ID` 响应头和结构化日志，
便于定位同一次请求：

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User not found"
  },
  "request_id": "d50d95f02b324876b8a45ca4db53fbb8"
}
```

## 测试与质量检查

测试通过依赖覆盖隔离数据库，默认不要求运行 PostgreSQL：

```powershell
Set-Location apps/api
uv run ruff format --check .
uv run ruff check .
uv run pytest --strict-markers
```

GitHub Actions 会在向 `main`、`dev` 推送或提交 Pull Request 时使用 `uv.lock`
执行同样的 Ruff 和 pytest 检查。前端工程尚未初始化，因此 CI 当前只检查后端。

## 数据库迁移

Alembic 使用 `DATABASE_URL` 连接数据库。首次启动或拉取到新迁移后执行：

```powershell
Set-Location apps/api
uv run alembic upgrade head
```

创建后续迁移时先修改 `app/models`，再运行：

```powershell
uv run alembic revision --autogenerate -m "describe change"
uv run alembic check
```

初始迁移创建 `users`、`workspaces` 与 `workspace_members` 表；用户邮箱和工作区
slug 全局唯一，成员角色限制为 `owner/admin/member/viewer`，成员记录随用户或工作区
删除而级联清理。

## 项目结构

```text
apps/api/app/
├── api/           # 路由与依赖注入
├── core/          # 配置、异常处理、日志和中间件
├── db/            # SQLAlchemy 会话与事务边界
├── models/        # 数据模型
├── repositories/  # 数据访问
├── schemas/       # 请求与响应模型
└── services/      # 业务逻辑
```

迁移脚本位于 `apps/api/alembic/versions`。

后续里程碑与退出标准见 [ROADMAP.md](ROADMAP.md)。
