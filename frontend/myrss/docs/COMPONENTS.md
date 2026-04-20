# 组件文档

## 概述

本文档详细说明 MyRSS 项目中各个 Vue 组件的功能、属性和使用方法。

## 组件关系图

```
App.vue
  └── MainLayout.vue
        ├── HeaderBar.vue
        ├── Sidebar.vue
        └── RouterView
              ├── HomeView.vue (默认)
              └── AboutView.vue (懒加载)
```

## 组件详细说明

### 1. App.vue (应用根组件)

**文件位置**: `src/App.vue`

**功能**: 应用根组件，提供全局样式和挂载主布局

**模板结构**:
```vue
<template>
  <MainLayout />
</template>
```

**样式特性**:
- 全局盒模型重置 (`margin: 0; padding: 0; box-sizing: border-box`)
- 字体优化和抗锯齿设置
- 基础 body 样式

**导入关系**:
- 导入: `MainLayout.vue`
- 导出: 无（根组件）

### 2. MainLayout.vue (主布局组件)

**文件位置**: `src/components/MainLayout.vue`

**功能**: 组织应用的整体布局结构

**布局特点**:
- 三栏布局：顶栏 + 侧边栏 + 内容区域
- 精确比例：侧边栏 10%，内容区域 90%
- 使用 CSS Grid 或 Flexbox 实现响应式布局

**模板结构**:
```vue
<template>
  <div class="main-layout">
    <HeaderBar />
    <div class="content-wrapper">
      <Sidebar />
      <main class="main-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>
```

**关键样式**:
```css
/* 精确的 10% + 90% 布局 */
.content-wrapper {
  display: flex;
  height: calc(100vh - 60px); /* 减去顶栏高度 */
}

.sidebar {
  width: 10%;
  min-width: 200px;
}

.main-content {
  width: 90%;
  flex: 1;
}
```

**导入关系**:
- 导入: `HeaderBar.vue`, `Sidebar.vue`, `RouterView` (Vue Router)
- 导出: 默认导出

### 3. HeaderBar.vue (顶部导航栏)

**文件位置**: `src/components/HeaderBar.vue`

**功能**: 显示应用 logo 和主题切换功能

**布局结构**:
- 左侧: "myrss" logo
- 右侧: 主题切换按钮 + GitHub 链接

**主要特性**:
1. **Logo 显示**: 使用文本或图片显示 "myrss"
2. **主题切换**: 支持亮色/暗色主题切换
3. **GitHub 链接**: 指向项目仓库
4. **响应式设计**: 适配不同屏幕宽度

**使用的 Naive UI 组件**:
- `NButton`: 按钮组件
- `NSpace`: 间距组件
- `NDropdown`: 下拉菜单（用于主题选择）

**代码示例**:
```vue
<script setup lang="ts">
import { Icon } from '@vicons/utils'
import { MoonOutline, SunnyOutline } from '@vicons/ionicons5'

// 主题状态管理
const isDark = ref(false)

// 主题切换函数
const toggleTheme = () => {
  isDark.value = !isDark.value
  // 应用主题变化
}
</script>
```

**导入关系**:
- 导入: `@vicons/utils`, `@vicons/ionicons5`, Naive UI 组件
- 导出: 默认导出

### 4. Sidebar.vue (侧边栏组件)

**文件位置**: `src/components/Sidebar.vue`

**功能**: 显示 RSS 源列表，提供导航功能

**主要特性**:
1. **数据获取**: 从 `http://127.0.0.1:8000/feed/sources` 获取 RSS 源数据
2. **列表显示**: 显示 RSS 源名称和图标
3. **状态管理**: 处理加载中、成功、错误状态
4. **导航功能**: 点击 RSS 源跳转到对应页面

**数据获取逻辑**:
```typescript
const sources = ref([])
const isLoading = ref(false)
const error = ref(null)

const fetchSources = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await fetch('http://127.0.0.1:8000/feed/sources')
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    sources.value = await response.json()
  } catch (err) {
    error.value = err.message
    // 显示错误提示
  } finally {
    isLoading.value = false
  }
}
```

**状态显示**:
- **加载中**: 显示加载指示器
- **成功**: 显示 RSS 源列表
- **错误**: 显示错误信息和重试按钮
- **空状态**: 显示暂无数据提示

**使用的 Naive UI 组件**:
- `NList`: 列表组件
- `NListItem`: 列表项组件
- `NSpin`: 加载指示器
- `NEmpty`: 空状态组件
- `NAlert`: 错误提示组件

**导入关系**:
- 导入: `@vicons/utils`, Naive UI 组件
- 导出: 默认导出

### 5. HomeView.vue (首页视图)

**文件位置**: `src/views/HomeView.vue`

**功能**: 应用首页，显示欢迎信息和统计

**内容结构**:
1. **欢迎标题**: 应用名称和欢迎语
2. **统计信息**: RSS 源数量、未读文章数等
3. **功能简介**: 应用主要功能说明
4. **快速操作**: 常用功能入口

**路由配置**:
- 路径: `/`
- 名称: `home`
- 类型: 默认路由，非懒加载

**使用的 Naive UI 组件**:
- `NCard`: 卡片组件
- `NStatistic`: 统计组件
- `NButton`: 按钮组件
- `NSpace`: 间距组件

**导入关系**:
- 导入: `Icon` (从 `@vicons/utils`), Naive UI 组件
- 导出: 默认导出

### 6. AboutView.vue (关于页面视图)

**文件位置**: `src/views/AboutView.vue`

**功能**: 显示项目相关信息

**内容结构**:
1. **项目标题**: 关于 MyRSS
2. **项目描述**: 应用功能和特点介绍
3. **技术栈**: 使用的技术和框架
4. **开发团队**: 贡献者信息
5. **版本信息**: 当前版本和更新日志

**路由配置**:
- 路径: `/about`
- 名称: `about`
- 类型: 懒加载路由，生成单独的代码块

**懒加载优势**:
- 减少首屏加载体积
- 提高首屏加载速度
- 按需加载，优化资源使用

**路由配置代码**:
```typescript
{
  path: '/about',
  name: 'about',
  component: () => import('../views/AboutView.vue')
}
```

**导入关系**:
- 无外部导入（懒加载组件）
- 导出: 默认导出

## 组件通信

### 1. Props (父向子)
- 当前使用较少，主要通过状态管理
- 未来可扩展为可配置组件

### 2. Events (子向父)
- 使用 Vue 的自定义事件系统
- 示例: `@theme-change`, `@source-select`

### 3. 状态管理
- 使用 Pinia 进行全局状态管理
- 当前使用响应式变量进行局部状态管理

### 4. Provide/Inject
- 可用于深层组件通信
- 当前未使用，但支持未来扩展

## 样式设计原则

### 1. 布局系统
- 使用 CSS Grid 和 Flexbox
- 实现精确的比例布局（10% + 90%）
- 响应式断点设计

### 2. 主题系统
- 基于 CSS 变量的主题切换
- 亮色/暗色主题支持
- 跟随系统主题设置

### 3. 组件样式
- 使用 Scoped CSS 防止样式冲突
- BEM 命名约定（可选）
- 使用 CSS 变量统一设计令牌

### 4. 响应式设计
- 移动端优先设计
- 断点: sm (640px), md (768px), lg (1024px), xl (1280px)
- 使用媒体查询适配不同设备

## 组件最佳实践

### 1. 单一职责
- 每个组件专注于单一功能
- 避免组件过于复杂

### 2. 可重用性
- 设计可配置的 Props 接口
- 提供合理的默认值
- 使用插槽增强灵活性

### 3. 可测试性
- 组件逻辑与视图分离
- 使用 Composition API 提高可测试性
- 提供清晰的输入输出接口

### 4. 性能优化
- 使用 `v-once` 处理静态内容
- 合理使用 `v-memo` 缓存计算结果
- 懒加载非关键组件

## 组件开发指南

### 1. 创建新组件
```bash
# 在 components 目录创建新组件
touch src/components/NewComponent.vue
```

### 2. 组件模板
```vue
<template>
  <!-- 组件模板 -->
</template>

<script setup lang="ts">
// 组件逻辑
</script>

<style scoped>
/* 组件样式 */
</style>
```

### 3. 类型定义
```typescript
// 定义 Props 接口
interface Props {
  title?: string
  items: Array<Item>
}

// 定义 Emits 接口  
interface Emits {
  (e: 'select', item: Item): void
}

// 使用 defineProps 和 defineEmits
const props = defineProps<Props>()
const emit = defineEmits<Emits>()
```

### 4. 组件注册
```typescript
// 局部注册（推荐）
import NewComponent from './components/NewComponent.vue'

// 在模板中使用
<NewComponent :items="items" @select="handleSelect" />
```

## 组件测试

### 1. 单元测试
```typescript
// 示例测试结构
describe('HeaderBar.vue', () => {
  it('显示正确的 logo', () => {
    // 测试逻辑
  })
  
  it('主题切换功能正常', () => {
    // 测试逻辑
  })
})
```

### 2. 测试工具
- **Vitest**: 测试框架
- **@vue/test-utils**: Vue 组件测试工具
- **Testing Library**: 用户行为测试

### 3. 测试覆盖率
- 组件逻辑覆盖率 > 80%
- 用户交互测试
- 边界条件测试

---

**文档版本**: v1.0  
**最后更新**: 2026年4月20日