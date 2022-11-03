<template>
 <div class="box">
   <div class="columns">
     <div class="column is-1" role="form" aria-label="Add">
       <input type="text" class="input" placeholder="Nota">
     </div>
     <div class="column is-1" role="form" aria-label="Add">
       <input type="text" class="input" placeholder="Nome">
     </div>
     <div class="column is-1" role="form" aria-label="Add">
       <input type="text" class="input" placeholder="Ativo">
     </div>
     <div class="column is-1" role="form" aria-label="Add">
       <input type="text" class="input" placeholder="Dividendos">
     </div>
     <div class="column is-2" role="form" aria-label="Add">
       <input type="text" class="input" placeholder="Atividade Econômica">
     </div>
   </div>
   <div class="columns">
     <div class="column is-1" role="form" aria-label="Add">
       <input type="text" class="input" placeholder="Setor">
     </div>
     <div class="column is-1" role="form" aria-label="Add">
       <input type="text" class="input" placeholder="País">
     </div>
     <div class="column is-1" role="form" aria-label="Add">
       <input type="text" class="input" placeholder="Continente">
     </div>
     <div class="column is-1" role="form" aria-label="Add">
       <input type="text" class="input" placeholder="Qtd. Ações">
     </div>
     <div class="column is-1" role="form" aria-label="Add">
       <input type="text" class="input" placeholder="Preço">
     </div>
     <div class="column">
       <button class="button">
            <span class="icon">
                <i class="fas fa-add"></i>
            </span>
            <span>Add</span>
        </button>
     </div>
   </div>
 </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({name: "FormAddAsset"})
</script>

<style scoped>

</style>