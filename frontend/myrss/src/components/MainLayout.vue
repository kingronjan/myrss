<script lang="ts" setup>

import Header from '@/components/layout/Header.vue'
import Main from '@/components/layout/Main.vue'

</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header><Header /></el-header>
      <el-container>
        <el-main><Main /></el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped></style>
