<script lang="ts" setup>
import { ref, onUnmounted, reactive } from 'vue'
import { Document, Refresh, Edit, Delete, Loading } from '@element-plus/icons-vue'
import { syncFeed, getSyncStatus, updateFeedSource, deleteFeedSource, type FeedSource } from '@/api/feed'
import { useFeedStore } from '@/stores/feed'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'

const props = defineProps<{
  source: FeedSource
}>()

const emit = defineEmits<{
  (e: 'updated'): void
  (e: 'deleted'): void
  (e: 'synced'): void
}>()

const isSyncing = ref(false)
const feedStore = useFeedStore()
let pollInterval: ReturnType<typeof setInterval> | null = null

// 编辑相关
const editDialogVisible = ref(false)
const editFormRef = ref<FormInstance>()
const editForm = reactive({
  description: '',
  url: ''
})

const rules = reactive<FormRules>({
  description: [
    { required: true, message: '请输入订阅源名称', trigger: 'blur' },
    { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' }
  ],
  url: [
    { required: true, message: '请输入订阅源 URL', trigger: 'blur' },
    { type: 'url', message: '请输入有效的 URL', trigger: 'blur' }
  ]
})

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
      openEditDialog()
      break
    case 'delete':
      handleDelete()
      break
  }
}

const openEditDialog = () => {
  editForm.description = props.source.description
  editForm.url = props.source.url
  editDialogVisible.value = true
}

const handleEditSave = async () => {
  if (!editFormRef.value) return
  
  await editFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await updateFeedSource(props.source.id, {
          description: editForm.description,
          url: editForm.url
        })
        ElMessage.success('更新成功')
        editDialogVisible.value = false
        emit('updated')
      } catch (error) {
        ElMessage.error('更新失败')
      }
    }
  })
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
  ).then(async () => {
    try {
      await deleteFeedSource(props.source.id)
      ElMessage.success('已删除')
      emit('deleted')
    } catch (error) {
      ElMessage.error('删除失败')
    }
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

    <!-- 编辑对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑订阅源"
      width="500px"
      append-to-body
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="rules"
        label-width="80px"
        @submit.prevent
      >
        <el-form-item label="名称" prop="description">
          <el-input v-model="editForm.description" placeholder="请输入订阅源名称" />
        </el-form-item>
        <el-form-item label="URL" prop="url">
          <el-input v-model="editForm.url" placeholder="请输入 RSS 链接" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleEditSave">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
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
