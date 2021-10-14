<template>
  <q-layout view="lHh lpR lFf">

    <q-header elevated class="bg-indigo-10 text-white" height-hint="100">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <q-btn round to="/">
            <q-avatar size="40px">
              <img class="logo-img" src="@/assets/clipboard.png"/>
            </q-avatar>
          </q-btn>
           Приложение для отправки задач в очередь
        </q-toolbar-title>
        <q-space />

        <!--      <q-tabs v-model="tab">-->
        <q-tabs v-if="!username  || username.length === 0"
                class="text-white" indicator-color="orange" shrink stretch>
          <q-route-tab name="username" icon="assignment_ind" label="Вход" to="/login" />
        </q-tabs>
        <q-tabs v-else class="text-white" indicator-color="orange" shrink stretch>
          <q-route-tab name="username" icon="assignment_ind" :label="username" to="/" />
          <q-tab @click.prevent="onLogout()" name="logout" label="Выйти" />
        </q-tabs>

      </q-toolbar>
    </q-header>

    <q-drawer
        v-model="leftDrawerOpen"
        show-if-above
        :width="300"
        :breakpoint="700"
        bordered
        class="bg-indigo-10 text-white">
      <q-scroll-area class="fit">
        <q-list padding class="menu-list" >
          <q-item clickable v-ripple to="/" active-class="text-orange">
            <q-item-section avatar>
              <q-icon name="inbox" />
            </q-item-section>

            <q-item-section>
              Главная страница
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="goToTasks()" to="/all_tasks" active-class="text-orange">
            <q-item-section avatar>
              <q-icon name="star" />
            </q-item-section>

            <q-item-section>
              Список задач
            </q-item-section>
          </q-item>

          <q-separator dark/>

          <q-item clickable v-ripple @click="loadTasks()" active-class="text-orange">
            <q-item-section avatar>
              <q-icon name="assignment" />
            </q-item-section>

            <q-item-section>
              Обновить список задач
            </q-item-section>
          </q-item>

          <q-separator dark/>

          <q-item clickable v-ripple v-for="(i, task) in filteredTasksList" :key="i">
            <q-item-section @click="goToTask(task)">{{ task }}</q-item-section>
            <q-item-section avatar>
              <q-avatar v-if="i === 'SUCCESS'" :color="colors.positive"></q-avatar>
              <q-avatar v-else-if="i === 'PROGRESS'" :color="colors.warning"></q-avatar>
              <q-avatar v-else-if="i === 'PENDING'" :color="colors.info"></q-avatar>
              <q-avatar v-else :color="colors.negative"></q-avatar>
            </q-item-section>
          </q-item>

        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'BasePage',
  data() {
    return {
      colors: {
        positive: 'positive',
        warning: 'warning',
        info: 'info',
        negative: 'negative'
      }
    }
  },
  computed: {
    username() {
      return this.$store.state.username;
    },
    filteredTasksList() {
      return this.$store.state.tasksList;
    }
  },
  setup() {
    const leftDrawerOpen = ref(false);

    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      }
    }
  },
  methods: {
    onLogout() {
      this.$store.dispatch('onLogout');
    },
    loadTasks() {
      this.$store.dispatch('loadTasks');
    },
    goToTasks() {
      this.$store.dispatch('getTasks');
    },
    goToTask(urlTask) {
      this.$store.dispatch('getTask', urlTask);
    }
  },
  beforeCreate() {
    this.$store.commit('initialiseStore');
  }
}
</script>