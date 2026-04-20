<script lang="ts" setup>
import { useFeedStore } from '@/stores/feed'
import { computed } from 'vue'

const feedStore = useFeedStore()

const stripHtml = (html: string) => {
  if (!html) return ''
  // 移除 HTML 标签
  const text = html.replace(/<[^>]*>?/gm, '')
  // 截取前 300 个字符
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

const feeds = computed(() => feedStore.feeds)
const loading = computed(() => feedStore.loading)
</script>

<template>
  <div class="content-container" v-loading="loading">
    <el-empty v-if="feeds.length === 0 && !loading" description="暂无数据" />
    <div v-else class="feed-list">
      <el-card v-for="item in feeds" :key="item.id" class="feed-item">
        <template #header>
          <div class="card-header">
            <span class="title">{{ item.title }}</span>
            <span class="time">{{ formatDate(item.published) }}</span>
          </div>
        </template>
        <div class="summary">
          {{ stripHtml(item.summary) }}
        </div>
        <div class="footer">
          <el-button type="primary" link @click="openLink(item.link)">
            查看原文
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.content-container {
  padding: 20px;
  height: 100%;
  overflow-y: auto;
}

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

.time {
  color: #999;
  font-size: 0.9em;
}

.summary {
  color: #666;
  line-height: 1.6;
  margin-bottom: 10px;
  white-space: pre-wrap;
  word-break: break-all;
}

.footer {
  display: flex;
  justify-content: flex-end;
}
</style>
