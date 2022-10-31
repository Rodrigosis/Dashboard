<template>
  <main>
    <main class="columns is-gapless is-multiline">
      <div class="column is-1">
        <CustomSideBar />
      </div>
      <div class="column is-11">
        <AssetsTable />
        <LineChart />
      </div>
    </main>
  </main>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import CustomSideBar from "@/components/CustomSideBar.vue";
import AssetsTable from "@/components/AssetsTable.vue";
import LineChart from "@/components/lineChart";

export default defineComponent({
  name: 'App',
  components: {LineChart, AssetsTable, CustomSideBar},
});
</script>

<style>

</style>
