# MyRSS 前端项目

## 项目状态

✅ **核心功能已完成**

基于 Vue 3 + TypeScript + Naive UI 构建的 RSS 阅读器前端应用，包含：

- 顶栏 + 侧边栏 + 内容区域的三栏布局
- 响应式设计，支持亮色/暗色主题切换
- 侧边栏从 API 获取 RSS 源数据
- 精确的 10% 侧边栏 + 90% 内容区域布局比例

## 快速开始

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 项目文档

完整的项目文档位于 `docs/` 目录：

### 📚 核心文档
- [项目概述](docs/README.md) - 项目概况、技术栈、文件结构
- [项目总结](docs/SUMMARY.md) - 里程碑、技术架构、后续规划

### 🔧 技术文档
- [API 接口文档](docs/API.md) - API 规范、数据格式、错误处理
- [组件文档](docs/COMPONENTS.md) - 组件说明、使用方式、通信机制
- [开发与部署指南](docs/DEVELOPMENT.md) - 环境设置、构建流程、部署方案

- [文档索引](docs/INDEX.md) - 所有文档的快速查找指南

## 项目结构

```
myrss/
├── docs/                    # 项目文档
├── src/                    # 源代码
│   ├── assets/            # 静态资源
│   ├── components/        # Vue组件
│   ├── router/           # 路由配置
│   ├── views/            # 页面视图
│   ├── App.vue           # 根组件
│   └── main.ts           # 入口文件
├── package.json          # 依赖配置
├── vite.config.ts        # 构建配置
└── tsconfig.json         # TypeScript配置
```

## 功能特性

### ✅ 已完成
- 响应式三栏布局（10% + 90% 精确比例）
- 主题切换（亮色/暗色，跟随系统）
- RSS 源数据获取和显示
- Vue Router 单页面应用
- 代码清理和优化

### 🚧 待开发
- RSS 文章阅读功能
- 用户认证系统
- 文章收藏和管理
- 离线阅读支持

## 技术栈

- **框架**: Vue 3 (Composition API)
- **语言**: TypeScript
- **UI 库**: Naive UI
- **图标**: @vicons/ionicons5
- **状态管理**: Pinia
- **路由**: Vue Router
- **构建工具**: Vite
- **测试**: Vitest + Playwright

## 构建与部署

### 开发
```bash
npm run dev          # 开发服务器
npm run type-check   # 类型检查
npm run lint         # 代码检查
```

### 构建
```bash
npm run build        # 生产构建
npm run preview      # 预览构建结果
```

### 部署
构建产物输出到 `../../static/` 目录，可部署到：
- 静态文件托管（Nginx、Apache）
- 云服务（Netlify、Vercel、AWS S3）
- 容器化部署（Docker + Nginx）

## 贡献指南

欢迎提交 Issue 和 Pull Request。在贡献代码前，请先阅读相关文档。

## 许可证

[MIT License](LICENSE)

---

**最后更新**: 2026年4月20日  
**项目状态**: 核心功能完成，可投入生产使用
