<script lang="ts" setup>

import Menu from './Menu.vue';

</script>

<template>
  <div>
    <el-splitter>
      <el-splitter-panel size="20%">
        <div class="demo-panel"><Menu /></div>
      </el-splitter-panel>
      <el-splitter-panel :min="200">
        <div class="demo-panel">2</div>
      </el-splitter-panel>
    </el-splitter>
  </div>
</template>

<style scoped>
.demo-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
