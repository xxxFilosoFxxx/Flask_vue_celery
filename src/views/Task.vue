<template>
    <div>
        <get-tasks></get-tasks>
    </div>
</template>

<script>
import GetTasks from "@/components/GetTasks";

export default {
    name: "Task",
    components: {
        GetTasks
    }
    // created() {
    //     this.$watch(
    //         () => this.$route.params,
    //         () => {
    //             this.currentTask
    //         },
    //         { immediate: true }
    //     )
    // }
}
</script>

<style scoped>

</style>