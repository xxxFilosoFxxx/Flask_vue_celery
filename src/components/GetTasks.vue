<template>
  <div class="q-pa-md">
    <q-table
      title="Задачи"
      :rows="rows"
      :columns="columns"
      row-key="name"
      hide-bottom
    />
  </div>
</template>

<script>
export default {
  name: "GetTasks",
  props: ['task'],
  data() {
    return {
      columns: [{
          name: 'name',
          required: true,
          label: 'Id Задачи',
          align: 'left',
          field: row => row.name,
          format: val => `${val}`,
          sortable: true
        },
        { name: 'msisdn', align: 'center', label: 'Msisdn', field: 'msisdn', sortable: true },
        { name: 'radius', label: 'Radius', field: 'radius', sortable: true },
        { name: 'delta', label: 'Delta', field: 'delta', sortable: true },
        { name: 'status', label: 'Status', field: 'status'}
      ],
      rows: [{
        name: this.$route.params.uuid,
        msisdn: this.task.msisdn,
        radius: this.task.radius,
        delta: this.task.delta,
        status: this.task.status
      }]
    }
  },
  // computed: {
  //   task() {
  //     return this.$store.state.currentTask;
  //   }
  // }
}
</script>
<style scoped>

</style>