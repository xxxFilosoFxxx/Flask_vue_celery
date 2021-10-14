<template>
  <div class="q-pa-md">
    <q-table
      title="Задачи"
      :rows="rows"
      :columns="columns"
      row-key="task_id"
    />
  </div>
</template>

<script>
export default {
  name: "GetAllTasks",
  data() {
    return {
      columns: [{
        name: 'task_id',
        required: true,
        label: 'Id Задачи',
        align: 'left',
        field: row => row['task_id'],
        format: val => `${val}`,
        sortable: true
        },
        { name: 'msisdn', align: 'center', label: 'Msisdn', field: 'msisdn', sortable: true },
        { name: 'radius', label: 'Radius', field: 'radius', sortable: true },
        { name: 'delta', label: 'Delta', field: 'delta', sortable: true },
        { name: 'status', label: 'Status', field: 'status'}
      ],
      rows: this.$store.state.allTasksList
    }
  }
}
</script>
<style scoped>

</style>