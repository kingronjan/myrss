# API 接口文档

## 概述

MyRSS 前端应用通过 REST API 与后端服务通信，获取 RSS 源数据。

## 数据获取接口

### 1. RSS 源数据获取

**接口地址**: `http://127.0.0.1:8000/feed/sources`

**请求方法**: GET

**响应格式**: JSON

**用途**: 获取所有可用的 RSS 源列表

**使用位置**: `src/components/Sidebar.vue`

**示例响应结构**:
```json
[
  {
    "id": 1,
    "name": "技术博客",
    "url": "https://example.com/feed.xml",
    "category": "technology",
    "last_updated": "2026-04-20T10:30:00Z"
  },
  {
    "id": 2,
    "name": "新闻聚合",
    "url": "https://news.example.com/rss",
    "category": "news",
    "last_updated": "2026-04-19T15:45:00Z"
  }
]
```

**字段说明**:
- `id`: 唯一标识符
- `name`: RSS 源名称
- `url`: RSS 源地址
- `category`: 分类（可选）
- `last_updated`: 最后更新时间（可选）

## 前端数据获取实现

### Sidebar.vue 中的数据获取代码

```typescript
// 从 API 获取 RSS 源数据
const fetchSources = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/feed/sources');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    sources.value = data;
  } catch (error) {
    console.error('Failed to fetch RSS sources:', error);
    // 可以显示错误提示
  }
};
```

### 错误处理机制

1. **网络错误**: 捕获 fetch 异常
2. **HTTP 错误**: 检查响应状态码
3. **数据解析错误**: JSON 解析失败处理
4. **超时处理**: 可以添加超时逻辑（当前未实现）

## 环境配置建议

当前 API 地址是硬编码的，建议改为环境变量：

```env
# .env.development
VITE_API_BASE_URL=http://127.0.0.1:8000

# .env.production
VITE_API_BASE_URL=https://api.example.com
```

使用方式：
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const response = await fetch(`${API_BASE_URL}/feed/sources`);
```

## 未来 API 扩展建议

### 1. 文章获取接口
```
GET /feed/{source_id}/articles
GET /feed/articles?source={source_id}&page={page}&limit={limit}
```

### 2. 用户相关接口
```
POST /auth/login
POST /auth/register
GET  /user/preferences
PUT  /user/preferences
```

### 3. 源管理接口
```
POST   /feed/sources
PUT    /feed/sources/{id}
DELETE /feed/sources/{id}
```

### 4. 文章操作接口
```
POST   /articles/{id}/read
POST   /articles/{id}/bookmark
POST   /articles/{id}/like
```

## 数据模型

### RSS 源模型 (Source)
```typescript
interface Source {
  id: number;
  name: string;
  url: string;
  description?: string;
  category?: string;
  icon?: string;
  is_active: boolean;
  last_fetched?: string;
  created_at: string;
  updated_at: string;
}
```

### 文章模型 (Article)
```typescript
interface Article {
  id: number;
  source_id: number;
  title: string;
  link: string;
  description?: string;
  content?: string;
  author?: string;
  published_at: string;
  thumbnail?: string;
  is_read: boolean;
  is_bookmarked: boolean;
  created_at: string;
}
```

## 分页和筛选

建议的查询参数：
- `page`: 页码（默认: 1）
- `limit`: 每页数量（默认: 20）
- `category`: 按分类筛选
- `sort`: 排序字段（如 `published_at`, `-published_at`）
- `search`: 搜索关键词

示例：`/feed/articles?page=1&limit=20&category=technology&sort=-published_at`

## 认证和授权

未来如果需要用户系统，建议：
- 使用 JWT 令牌认证
- 在请求头中添加 `Authorization: Bearer {token}`
- 实现令牌刷新机制

## 错误响应格式

建议的统一错误响应：
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "请求的资源不存在",
    "details": {}
  }
}
```

## 版本控制

建议 API 支持版本控制：
- `/api/v1/feed/sources`
- 通过 Accept 头部指定版本：`Accept: application/vnd.myrss.v1+json`

---

**文档版本**: v1.0  
**最后更新**: 2026年4月20日