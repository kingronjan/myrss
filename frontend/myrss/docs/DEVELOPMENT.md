# 开发与部署指南

## 开发环境设置

### 1. 系统要求

- **Node.js**: 18.x 或更高版本
- **npm**: 9.x 或更高版本（或使用 yarn/pnpm）
- **Git**: 版本控制

### 2. 环境检查

```bash
# 检查 Node.js 版本
node --version

# 检查 npm 版本
npm --version

# 检查 Git 版本
git --version
```

### 3. 项目克隆与初始化

```bash
# 克隆项目
git clone <repository-url>
cd myrss/frontend/myrss

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 开发工作流程

### 1. 日常开发

```bash
# 启动开发服务器（热重载）
npm run dev

# 浏览器自动打开 http://localhost:5173
```

### 2. 代码质量检查

```bash
# 运行代码检查
npm run lint

# 修复可自动修复的问题
npm run lint:fix

# 类型检查
npm run type-check

# 运行所有检查
npm run check
```

### 3. 组件开发

#### 创建新组件
```bash
# 在 components 目录创建组件
touch src/components/NewComponent.vue

# 在 views 目录创建页面
touch src/views/NewPage.vue
```

#### 组件开发规范
1. **使用 Composition API**: 优先使用 `<script setup>`
2. **类型安全**: 使用 TypeScript 定义接口
3. **样式作用域**: 使用 `scoped` CSS
4. **组件通信**: 使用 Props/Emits 或 Pinia

### 4. API 开发

#### 数据获取示例
```typescript
// 使用 Fetch API
const fetchData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/data')
    const data = await response.json()
    return data
  } catch (error) {
    console.error('数据获取失败:', error)
    throw error
  }
}
```

#### 环境变量配置
```env
# .env.local
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=MyRSS Development
```

```typescript
// 使用环境变量
const apiUrl = import.meta.env.VITE_API_BASE_URL
```

## 构建与测试

### 1. 构建流程

```bash
# 开发构建（带源映射）
npm run build:dev

# 生产构建
npm run build

# 预览构建结果
npm run preview
```

### 2. 构建配置

#### vite.config.ts 关键配置
```typescript
export default defineConfig({
  // 构建输出目录
  build: {
    outDir: '../../static',
    emptyOutDir: true,
  },
  
  // 基础路径
  base: '/static/',
  
  // 路径别名
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### 3. 测试流程

```bash
# 运行单元测试
npm run test:unit

# 运行 E2E 测试
npm run test:e2e

# 运行所有测试
npm run test
```

#### 测试文件结构
```
src/
├── components/
│   ├── __tests__/
│   │   └── ComponentName.spec.ts
└── views/
    └── __tests__/
        └── ViewName.spec.ts
```

## 部署指南

### 1. 生产环境构建

```bash
# 1. 确保代码是最新版本
git pull origin main

# 2. 安装依赖（生产环境）
npm ci --only=production

# 3. 运行生产构建
npm run build

# 4. 验证构建结果
ls -la ../../static/
```

### 2. 部署选项

#### 选项 A: 静态文件托管
```bash
# 构建输出到 ../../static/
# 可以将此目录部署到:
# - Nginx/Apache
# - GitHub Pages
# - Netlify/Vercel
# - AWS S3 + CloudFront
```

#### 选项 B: Docker 部署
```dockerfile
# Dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### 选项 C: 与后端集成
```nginx
# Nginx 配置示例
server {
    listen 80;
    server_name myrss.example.com;
    
    # 前端静态文件
    location /static/ {
        alias /path/to/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # 后端 API 代理
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # SPA 路由回退
    location / {
        try_files $uri $uri/ /static/index.html;
    }
}
```

### 3. 环境配置

#### 生产环境变量
```env
# .env.production
VITE_API_BASE_URL=https://api.myrss.example.com
VITE_APP_TITLE=MyRSS
VITE_APP_VERSION=1.0.0
```

#### 构建时注入
```bash
# 使用特定环境文件
npm run build -- --mode production
```

### 4. 部署验证清单

- [ ] 构建成功，无错误
- [ ] 静态文件生成在正确目录
- [ ] 环境变量正确配置
- [ ] API 端点可访问
- [ ] 路由回退配置正确
- [ ] 缓存策略合理
- [ ] SSL/TLS 证书有效
- [ ] CDN 配置正确（如使用）

## 监控与维护

### 1. 性能监控

#### Lighthouse 检查
```bash
# 安装 Lighthouse CLI
npm install -g lighthouse

# 运行性能检查
lighthouse http://localhost:5173 --view
```

#### 关键性能指标
- **首字节时间 (TTFB)**: < 200ms
- **首次内容绘制 (FCP)**: < 1.5s
- **最大内容绘制 (LCP)**: < 2.5s
- **累积布局偏移 (CLS)**: < 0.1
- **首次输入延迟 (FID)**: < 100ms

### 2. 错误监控

#### 前端错误捕获
```typescript
// 全局错误处理
window.addEventListener('error', (event) => {
  console.error('全局错误:', event.error)
  // 发送到错误监控服务
})

// Promise 错误处理
window.addEventListener('unhandledrejection', (event) => {
  console.error('未处理的 Promise 错误:', event.reason)
})
```

#### 推荐监控服务
- **Sentry**: 错误追踪
- **LogRocket**: 会话重放
- **Google Analytics**: 用户分析

### 3. 版本管理

#### 版本号规范
- **主版本**: 不兼容的 API 修改
- **次版本**: 向下兼容的功能新增
- **修订号**: 向下兼容的问题修正

#### 发布流程
```bash
# 1. 更新版本号
npm version patch  # 或 minor, major

# 2. 构建发布版本
npm run build

# 3. 创建 Git 标签
git push --tags

# 4. 更新 CHANGELOG.md
```

## 故障排除

### 常见问题

#### 1. 构建失败
```bash
# 清理缓存
rm -rf node_modules/.vite
rm -rf node_modules/.cache

# 重新安装依赖
npm ci

# 重新构建
npm run build
```

#### 2. 开发服务器无法启动
```bash
# 检查端口占用
lsof -i :5173

# 使用不同端口
npm run dev -- --port 3000
```

#### 3. 类型检查错误
```bash
# 更新类型定义
npm run type-check -- --watch

# 修复常见类型问题
npm run type-check -- --noEmit
```

#### 4. 路由问题
- 检查 `router/index.ts` 配置
- 验证路由路径是否正确
- 检查 SPA 回退配置

### 调试工具

#### 浏览器开发者工具
- **Vue DevTools**: 组件调试
- **Network**: API 请求监控
- **Console**: JavaScript 错误
- **Performance**: 性能分析

#### VS Code 调试
```json
// launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Vue: Chrome",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/src"
    }
  ]
}
```

## 最佳实践

### 1. 代码组织
- **按功能分组**: 相关文件放在一起
- **统一命名**: 使用一致的命名约定
- **文档注释**: 为复杂逻辑添加注释

### 2. 性能优化
- **代码分割**: 路由懒加载
- **图片优化**: 使用 WebP 格式
- **缓存策略**: 合理设置 HTTP 缓存
- **Bundle 分析**: 使用 rollup-plugin-visualizer

### 3. 安全性
- **依赖更新**: 定期更新依赖包
- **环境变量**: 敏感信息不提交到仓库
- **CSP 配置**: 内容安全策略
- **XSS 防护**: 数据转义和验证

### 4. 可访问性
- **语义化 HTML**: 正确使用 HTML 标签
- **ARIA 属性**: 增强屏幕阅读器支持
- **键盘导航**: 支持键盘操作
- **颜色对比**: WCAG 2.1 AA 标准

## 持续集成/持续部署 (CI/CD)

### GitHub Actions 示例
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run build
      - run: npm run test
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

### 部署流水线
1. **代码提交** → 触发 CI
2. **运行测试** → 单元测试 + E2E 测试
3. **构建应用** → 生产环境构建
4. **安全扫描** → 依赖安全检查
5. **部署上线** → 自动部署到服务器

---

**文档版本**: v1.0  
**最后更新**: 2026年4月20日