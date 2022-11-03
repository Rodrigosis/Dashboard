<template>
 <div class="box">
   <div class="columns">
     <div class="column is-2">
       <button class="button is-success is-light" @click="compra">
            <span>Adicionar Compra</span>
        </button>
     </div>
     <div class="column is-2">
       <button class="button is-danger is-light"  @click="venda">
            <span>Adicionar Venda</span>
        </button>
      </div>
     <div class="column is-2">
       <button class="button is-info is-light"  @click="dividendos">
            <span>Adicionar Dividendos</span>
        </button>
     </div>
     <div class="column is-2">
       <button class="button is-primary is-light"  @click="atualizar">
            <span>Atualizar Dados</span>
        </button>
     </div>
   </div>
 </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
  name: "CustomHeader",
  methods: {
    compra () {
      console.log('compra')
    },
    venda () {
      console.log('venda')
    },
    dividendos () {
      console.log('dividendos')
    },
    atualizar () {
      console.log('atualizar')
    }
  }
})
</script>

<style scoped>

</style>