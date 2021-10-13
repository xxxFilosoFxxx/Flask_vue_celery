<template>
  <div class="q-pa-md">
    <q-table
      title="Задача"
      :rows="rows"
      :columns="columns"
      row-key="id"
      hide-bottom
    />
  </div>
</template>

<script>
export default {
  name: "GetTasks",
  data() {
    return {
      columns: [{
        name: 'id',
        required: true,
        label: 'Id Задачи',
        align: 'left',
        field: row => row.id,
        format: val => `${val}`
        },
        { name: 'msisdn', align: 'center', label: 'Msisdn', field: 'msisdn'},
        { name: 'radius', label: 'Radius', field: 'radius'},
        { name: 'delta', label: 'Delta', field: 'delta'},
        { name: 'status', label: 'Status', field: 'status'}
      ],
      rows: [this.$store.state.currentTask]
    }
  }
}
</script>
<style scoped>

</style>