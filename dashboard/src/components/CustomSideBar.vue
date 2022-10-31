<template>
  <div class="sidebar">
    <h1>
      <img src="../assets/logo.png" alt="">
    </h1>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({name: "CustomSideBar"})
</script>

<style scoped>
.sidebar {
  padding: 1rem;
  background-color: azure;
  width: 100%;
  height: 100vh;
}

@media only screen and (max-width: 768px){
  .sidebar {
    padding: 2.5rem;
    height: auto;
  }
}
</style>