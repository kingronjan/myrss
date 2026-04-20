# 默认环境（可以在运行命令时通过 ENV=production 覆盖）
ENV ?= dev

.PHONY: current migrations migrate dev help

# 查看当前迁移版本
current:
	uv run alembic current

# 生成迁移文件 (用法: make rev m="add_user_table")
# 如果没有提供 m 参数，会报错提示
migrations:
	@DESC="$(m)"; \
	if [ -z "$$DESC" ]; then \
		DESC="auto_$$(date +%Y%m%d%H%M)"; \
	fi; \
	uv run alembic revision --autogenerate -m "$$DESC"

# 执行迁移到最新版本
migrate:
	uv run alembic upgrade head
	
# 生成迁移文件，并执行迁移到最新版本
db-update: migrations migrate

# 运行 FastAPI 开发服务器
dev:
	uv run fastapi dev --reload-dir app

# 构建
build:
	cd frontend/myrss && npm run build

# 帮助信息
help:
	@echo "可用命令:"
	@echo "  make current  - 查看数据库当前迁移版本"
	@echo "  make migrations m='msg' - 自动生成迁移文件"
	@echo "  make migrate  - 执行所有未挂起的迁移"
	@echo "	 make db-update - 生成迁移文件，然后执行迁移"
	@echo "  make dev      - 启动 FastAPI 开发服务器"