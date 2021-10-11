<template>
    <div>
        <get-tasks :task="$store.state.currentTask"></get-tasks>
    </div>
</template>

<script>
import GetTasks from "@/components/GetTasks";

export default {
    name: "Task",
    components: {
        GetTasks
    }
}
</script>

<style scoped>

</style>