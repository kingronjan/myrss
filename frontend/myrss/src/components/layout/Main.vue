<script lang="ts" setup>

import Content from './Content.vue';
import Menu from './Menu.vue';

</script>

<template>
  <div class="main-wrapper">
    <el-splitter style="height: 100%">
      <el-splitter-panel size="30%">
        <div class="demo-panel"><Menu /></div>
      </el-splitter-panel>
      <el-splitter-panel :min="200">
        <div class="demo-panel"><Content /></div>
      </el-splitter-panel>
    </el-splitter>
  </div>
</template>

<style scoped>
.main-wrapper {
  height: 100%;
  width: 100%;
}
.demo-panel {
  height: 100%;
  width: 100%;
}
</style>
