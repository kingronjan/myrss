<script lang="ts" setup>
import { useFeedStore } from '@/stores/feed'
import { computed, ref, watch, nextTick } from 'vue'
import { ArrowLeft, Picture } from '@element-plus/icons-vue'

const feedStore = useFeedStore()
const scrollContainer = ref<HTMLElement | null>(null)

const scrollToTop = () => {
  nextTick(() => {
    if (scrollContainer.value) {
      scrollContainer.value.scrollTop = 0
    }
  })
}

// 监听详情切换，重置滚动条
watch(() => feedStore.selectedFeed, () => {
  scrollToTop()
})

// 监听列表数据变化（切换 source），重置滚动条
watch(() => feedStore.feeds, () => {
  scrollToTop()
})

const stripHtml = (html: string) => {
  if (!html) return ''
  // 1. 移除 HTML 标签
  let text = html.replace(/<[^>]*>?/gm, '')
  // 2. 移除空白行
  text = text.replace(/^\s*[\r\n]/gm, '').trim()
  // 3. 截取前 300 个字符
  return text.length > 300 ? text.substring(0, 300) + '...' : text
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString()
}

const openLink = (url: string) => {
  window.open(url, '_blank')
}

const selectFeed = (item: any) => {
  feedStore.selectedFeed = item
}

const goBack = () => {
  feedStore.selectedFeed = null
}

const sanitizeHtml = (html: string) => {
  if (!html) return ''
  // 移除 <script> 标签及其内容
  return html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
}

const feeds = computed(() => feedStore.feeds)
const loading = computed(() => feedStore.loading)
const selectedFeed = computed(() => feedStore.selectedFeed)
</script>

<template>
  <div ref="scrollContainer" class="content-container" v-loading="loading">
    <!-- 详情视图 (只在非加载状态下显示详情) -->
    <div v-if="selectedFeed && !loading" class="feed-detail">
      <div class="detail-header">
        <el-button :icon="ArrowLeft" @click="goBack" plain size="small">返回列表</el-button>
        <h2 class="detail-title">{{ selectedFeed.title }}</h2>
        <div class="detail-meta">
          <span>发布时间：{{ formatDate(selectedFeed.published) }}</span>
          <el-button type="primary" link @click="openLink(selectedFeed.link)">查看原文</el-button>
        </div>
      </div>
      <el-divider />
      <div class="detail-body" v-html="sanitizeHtml(selectedFeed.content)"></div>
    </div>

    <!-- 列表视图 -->
    <template v-else>
      <el-empty v-if="feeds.length === 0 && !loading" description="暂无数据" />
      <div v-else class="feed-list">
        <el-card v-for="item in feeds" :key="item.id" class="feed-item">
          <template #header>
            <div class="card-header">
              <span class="title clickable" @click="selectFeed(item)">{{ item.title }}</span>
              <span class="time">{{ formatDate(item.published) }}</span>
            </div>
          </template>
          <div class="feed-body">
            <div class="summary">
              {{ stripHtml(item.summary) }}
            </div>
            <el-image
              v-if="item.cover_url"
              :src="item.cover_url"
              fit="cover"
              class="feed-cover"
              lazy
            >
              <template #error>
                <div class="image-slot">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </div>
          <div class="footer">
            <el-button type="primary" link @click="openLink(item.link)">
              查看原文
            </el-button>
          </div>
        </el-card>
      </div>
    </template>
  </div>
</template>

<style scoped>
.content-container {
  padding: 20px;
  height: 100%;
  overflow-y: auto;
}

/* 列表样式 */
.feed-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feed-item {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-weight: bold;
  font-size: 1.1em;
}

.title.clickable {
  cursor: pointer;
  color: var(--el-color-primary);
  transition: opacity 0.2s;
}

.title.clickable:hover {
  text-decoration: underline;
  opacity: 0.8;
}

.time {
  color: #999;
  font-size: 0.9em;
}

.feed-body {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.summary {
  flex: 1;
  color: #666;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-all;
}

.feed-cover {
  width: 150px;
  height: 100px;
  border-radius: 4px;
  flex-shrink: 0;
  border: 1px solid var(--el-border-color-lighter);
}

.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
}

.footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

/* 详情页样式 */
.feed-detail {
  max-width: 800px;
  margin: 0 auto;
  padding-bottom: 50px;
}

.detail-header {
  margin-bottom: 20px;
}

.detail-title {
  margin: 20px 0 10px;
  font-size: 1.8em;
  line-height: 1.4;
}

.detail-meta {
  color: #999;
  font-size: 0.9em;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-body {
  line-height: 1.8;
  font-size: 1.1em;
  color: var(--el-text-color-primary);
}

.detail-body :deep(p) {
  margin: 0;
  padding-bottom: 1.2em;
}

/* 深度选择器确保渲染出的 HTML 图片和内容不溢出 */
.detail-body :deep(img) {
  max-width: 100%;
  height: auto;
}

.detail-body :deep(pre) {
  background: #f4f4f4;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
}

/* 暗黑模式适配预览（如果项目支持） */
:root.dark .detail-body :deep(pre) {
  background: #2d2d2d;
}
</style>
