<script lang="ts" setup>
import { ref, onUnmounted } from 'vue'
import { Document, Refresh, Edit, Delete, Loading } from '@element-plus/icons-vue'
import { syncFeed, getSyncStatus, type FeedSource } from '@/api/feed'
import { useFeedStore } from '@/stores/feed'
import { ElMessage, ElMessageBox } from 'element-plus'

const props = defineProps<{
  source: FeedSource
}>()

const emit = defineEmits<{
  (e: 'edit', source: FeedSource): void
  (e: 'delete', source: FeedSource): void
  (e: 'synced'): void
}>()

const isSyncing = ref(false)
const feedStore = useFeedStore()
let pollInterval: ReturnType<typeof setInterval> | null = null

const onContextMenu = () => {
  // 模拟一个全局点击，迫使其他已打开的 el-dropdown 关闭
  document.body.click()
}

const handleCommand = (command: string) => {
  switch (command) {
    case 'sync':
      handleSync()
      break
    case 'edit':
      emit('edit', props.source)
      break
    case 'delete':
      handleDelete()
      break
  }
}

const handleSync = async () => {
  if (isSyncing.value) {
    ElMessage.info(`订阅源 "${props.source.description || props.source.url}" 正在同步中...`)
    return
  }

  try {
    await syncFeed(props.source.id)
    isSyncing.value = true
    ElMessage.success(`已开始同步: ${props.source.description || props.source.url}`)

    pollInterval = setInterval(async () => {
      try {
        const statusData = await getSyncStatus(props.source.id)
        if (statusData.sync_status !== 1) {
          stopPolling()
          isSyncing.value = false

          if (statusData.sync_status === 2) {
            ElMessage.success('同步成功')
            emit('synced')
            if (feedStore.selectedFeedSourceId === props.source.id) {
              feedStore.fetchFeeds(props.source.id)
            }
          } else {
            ElMessage.error(`同步失败: ${statusData.sync_msg || '未知原因'}`)
          }
        }
      } catch (error) {
        stopPolling()
        isSyncing.value = false
        ElMessage.error('获取同步进度失败')
      }
    }, 2000)
  } catch (error) {
    ElMessage.error('启动同步失败')
  }
}

const stopPolling = () => {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

const handleDelete = () => {
  ElMessageBox.confirm(
    `确定要删除订阅源 "${props.source.description || props.source.url}" 吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    emit('delete', props.source)
    ElMessage.success('已删除')
  }).catch(() => {})
}

onUnmounted(() => {
  stopPolling()
})
</script>

<template>
  <div class="source-item-wrapper" @contextmenu="onContextMenu">
    <el-dropdown
      trigger="contextmenu"
      @command="handleCommand"
      class="source-dropdown"
    >
      <div class="source-item-content">
        <el-icon><document /></el-icon>
        <span class="source-title">{{ source.description || source.url }}</span>
        <el-icon v-if="isSyncing" class="is-loading sync-loading">
          <Loading />
        </el-icon>
      </div>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item command="sync" :disabled="isSyncing">
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
  </div>
</template>

<style scoped>
.source-item-wrapper {
  width: 100%;
  height: 100%;
}

.source-dropdown {
  width: 100%;
  height: 100%;
  display: block;
  line-height: inherit;
  color: inherit;
}

.source-item-content {
  width: 100%;
  height: 100%;
  padding: 0 20px 0 45px;
  display: flex;
  align-items: center;
  box-sizing: border-box;
  cursor: pointer;
}

.source-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sync-loading {
  margin-left: 10px;
  color: var(--el-color-primary);
}

/* 关键修复：确保 el-dropdown 的触发器容器填满整个高度 */
:deep(.el-tooltip__trigger) {
  width: 100%;
  height: 100%;
  outline: none;
  display: flex;
  align-items: center;
}
</style>
