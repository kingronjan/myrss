<script lang="ts" setup>
import { onMounted, ref, reactive } from 'vue'
import { Menu as IconMenu, Plus } from '@element-plus/icons-vue'
import { getFeedSources, addFeedSource, type FeedSource } from '@/api/feed'
import { useFeedStore } from '@/stores/feed'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import SourceItem from './SourceItem.vue'

const sources = ref<FeedSource[]>([])
const loading = ref(false)
const feedStore = useFeedStore()

// 新增相关
const addDialogVisible = ref(false)
const addFormRef = ref<FormInstance>()
const addForm = reactive({
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

const handleRefresh = () => {
  fetchSources()
}

const openAddDialog = () => {
  addForm.description = ''
  addForm.url = ''
  addDialogVisible.value = true
}

const handleAddSave = async () => {
  if (!addFormRef.value) return
  
  await addFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await addFeedSource({
          description: addForm.description,
          url: addForm.url
        })
        ElMessage.success('添加成功')
        addDialogVisible.value = false
        fetchSources()
      } catch (error) {
        ElMessage.error('添加失败')
      }
    }
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
        <div class="menu-title-container">
          <el-icon><icon-menu /></el-icon>
          <span>订阅源</span>
        </div>
      </template>
      <el-menu-item
        v-for="source in sources"
        :key="source.id"
        :index="String(source.id)"
        @click="handleSelect(source.id)"
        class="source-menu-item"
      >
        <SourceItem
          :source="source"
          @updated="handleRefresh"
          @deleted="handleRefresh"
          @synced="() => {}"
        />
      </el-menu-item>
      
      <el-menu-item index="add-source" @click="openAddDialog">
        <el-icon><plus /></el-icon>
        <span>新增订阅源</span>
      </el-menu-item>
    </el-sub-menu>
  </el-menu>

  <!-- 新增对话框 -->
  <el-dialog
    v-model="addDialogVisible"
    title="新增订阅源"
    width="500px"
    append-to-body
  >
    <el-form
      ref="addFormRef"
      :model="addForm"
      :rules="rules"
      label-width="80px"
      @submit.prevent
    >
      <el-form-item label="名称" prop="description">
        <el-input v-model="addForm.description" placeholder="请输入订阅源名称" />
      </el-form-item>
      <el-form-item label="URL" prop="url">
        <el-input v-model="addForm.url" placeholder="请输入 RSS 链接" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="addDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAddSave">
          确认
        </el-button>
      </span>
    </template>
  </el-dialog>
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

.menu-title-container {
  display: flex;
  align-items: center;
  width: 100%;
}
</style>
