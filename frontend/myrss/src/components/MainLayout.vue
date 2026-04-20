<script lang="ts" setup>

import Header from '@/components/layout/Header.vue'
import Main from '@/components/layout/Main.vue'

</script>

<template>
  <div class="common-layout">
    <el-container class="full-height">
      <el-header height="60px"><Header /></el-header>
      <el-container class="main-container">
        <el-main><Main /></el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.common-layout, .full-height {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-container {
  flex: 1;
  overflow: hidden;
  height: 0; /* Ensure it doesn't expand beyond parent */
}

:deep(.el-header) {
  padding: 0 20px;
}

:deep(.el-main) {
  padding: 0;
  height: 100%;
}
</style>
