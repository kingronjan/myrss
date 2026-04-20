<script lang="ts" setup>

import Content from './Content.vue';
import Menu from './Menu.vue';

</script>

<template>
  <div>
    <el-splitter>
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
.demo-panel {
  height: 100%;
  width: 100%;
}
</style>
