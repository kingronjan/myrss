<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { Document, Menu as IconMenu, Refresh, Edit, Delete, Loading } from '@element-plus/icons-vue'
import { getFeedSources, syncFeed, getSyncStatus, type FeedSource } from '@/api/feed'
import { useFeedStore } from '@/stores/feed'
import { ElMessage, ElMessageBox } from 'element-plus'

const sources = ref<FeedSource[]>([])
const loading = ref(false)
const syncingSources = ref(new Set<number>())
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
  feedStore.selectedFeed = null
  feedStore.fetchFeeds(sourceId)
}

const onContextMenu = () => {
  // 模拟一个全局点击，迫使其他已打开的 el-dropdown 关闭
  document.body.click()
}

const handleCommand = (command: string, source: FeedSource) => {
  switch (command) {
    case 'sync':
      handleSync(source)
      break
    case 'edit':
      handleEdit(source)
      break
    case 'delete':
      handleDelete(source)
      break
  }
}

const handleSync = async (source: FeedSource) => {
  if (syncingSources.value.has(source.id)) {
    ElMessage.info(`订阅源 "${source.description || source.url}" 正在同步中...`)
    return
  }

  try {
    await syncFeed(source.id)
    syncingSources.value.add(source.id)
    ElMessage.success(`已开始同步: ${source.description || source.url}`)

    // Start polling
    const pollInterval = setInterval(async () => {
      try {
        const statusData = await getSyncStatus(source.id)
        // 0 pending, 1 running, 2 success, 3 failed, 4 unset
        if (statusData.sync_status !== 1) {
          clearInterval(pollInterval)
          syncingSources.value.delete(source.id)

          if (statusData.sync_status === 2) {
            ElMessage.success('同步成功')
            // Refresh feeds if currently viewing this source
            if (feedStore.selectedFeedSourceId === source.id) {
              feedStore.fetchFeeds(source.id)
            }
          } else {
            ElMessage.error(`同步失败: ${statusData.sync_msg || '未知原因'}`)
          }
        }
      } catch (error) {
        clearInterval(pollInterval)
        syncingSources.value.delete(source.id)
        ElMessage.error('获取同步进度失败')
      }
    }, 1000)
  } catch (error) {
    ElMessage.error('启动同步失败')
  }
}

const handleEdit = (source: FeedSource) => {
  ElMessage.info(`编辑订阅源: ${source.description || source.url}`)
}

const handleDelete = (source: FeedSource) => {
  ElMessageBox.confirm(
    `确定要删除订阅源 "${source.description || source.url}" 吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    ElMessage.success('已删除')
  }).catch(() => {
    // Cancelled
  })
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
        class="source-menu-item"
      >
        <el-dropdown
          trigger="contextmenu"
          @command="(cmd) => handleCommand(cmd, source)"
          class="source-dropdown"
          @contextmenu="onContextMenu"
        >
          <div class="source-item-content">
            <el-icon><document /></el-icon>
            <span>{{ source.description || source.url }}</span>
            <el-icon v-if="syncingSources.has(source.id)" class="is-loading sync-loading">
              <Loading />
            </el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="sync" :disabled="syncingSources.has(source.id)">
                <el-icon><refresh /></el-icon>同步
              </el-dropdown-item>
              <el-dropdown-item command="edit">
                <el-icon><edit /></el-icon>编辑
              </el-dropdown-item>
              <el-dropdown-item command="delete" divided style="color: var(--el-color-danger)">
                <el-icon><delete /></el-icon>删除
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
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

.source-menu-item {
  padding: 0 !important;
}

.source-dropdown {
  width: 100%;
  height: 100%;
  display: block;
}

.source-item-content {
  width: 100%;
  height: 100%;
  padding: 0 20px 0 45px; /* Adjust padding to match standard menu item */
  display: flex;
  align-items: center;
  box-sizing: border-box;
  cursor: pointer;
}

.source-item-content span {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sync-loading {
  margin-left: 10px;
  color: var(--el-color-primary);
}

:deep(.el-dropdown) {
  line-height: inherit;
  color: inherit;
  display: block;
  height: 100%;
}

:deep(.el-tooltip__trigger) {
  width: 100%;
  height: 100%;
  outline: none;
  display: flex;
  align-items: center;
}
</style>
