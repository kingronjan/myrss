<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { Document, Menu as IconMenu } from '@element-plus/icons-vue'
import { getFeedSources, type FeedSource } from '@/api/feed'
import { useFeedStore } from '@/stores/feed'

const sources = ref<FeedSource[]>([])
const loading = ref(false)
const feedStore = useFeedStore()

const fetchSources = async () => {
  loading.value = true
  try {
    const data = await getFeedSources()
    sources.value = Array.isArray(data) ? data : []
  } catch (error) {
    console.error('Failed to fetch sources:', error)
  } finally {
    loading.value = false
  }
}

const handleSelect = (sourceId: number) => {
  feedStore.fetchFeeds(sourceId)
}

onMounted(() => {
  fetchSources()
})
</script>

<template>
  <el-menu
    default-active="0"
    class="el-menu-vertical-demo"
    v-loading="loading"
    :default-openeds="['sources-menu']"
  >
    <el-sub-menu index="sources-menu">
      <template #title>
        <el-icon><icon-menu /></el-icon>
        <span>订阅源</span>
      </template>
      <el-menu-item
        v-for="source in sources"
        :key="source.id"
        :index="String(source.id)"
        @click="handleSelect(source.id)"
      >
        <el-icon><document /></el-icon>
        <template #title>
          <span>{{ source.description || source.url }}</span>
        </template>
      </el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<style scoped>
.el-menu-vertical-demo {
  width: 100%;
  border-right: none;
  height: 100%;
}
</style>
