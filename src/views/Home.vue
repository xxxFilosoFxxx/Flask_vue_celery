<template>
  <div class="home">
    <InputParameters/>
  </div>
</template>

<script>

import InputParameters from "@/components/InputParameters";

export default {
  name: 'Home',
  components: {
    InputParameters
  }
}
</script>

<style lang="scss">
  @import "src/styles/quasar";
  @import "src/styles/quasar.variables.sass";

  body {
    background-color: $grey-2;
  }

  .logo-img {
    cursor: pointer;
    transition: 0.5s linear;
  }
  .logo-img:hover {
    -webkit-transform: scale(0.9);
    transform: scale(0.9);
  }
</style>
