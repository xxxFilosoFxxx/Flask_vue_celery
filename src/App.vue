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
<!--      // TODO: прописать ссылки к выпадающим задачам-->
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

          <q-item clickable v-ripple to="/about" active-class="text-orange">
            <q-item-section avatar>
              <q-icon name="star" />
            </q-item-section>

            <q-item-section>
              Список задач
            </q-item-section>
          </q-item>

          <q-separator dark/>

          <q-item clickable v-ripple v-for="n in 5" :key="n">
            <q-item-section>`Здесь появляется задача`</q-item-section>
            <q-item-section avatar>
              <q-avatar color="positive"></q-avatar>
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
import { io } from 'socket.io-client'
import { mapMutations } from 'vuex'

export default {
  name: 'BasePage',
  computed: {
    username() {
      return this.$store.state.username;
    },
    connected() {
      return this.$store.state.connect;
    },
    ...mapMutations(['connect'])
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
      // io.in(this.username).leave();
    }
  },
  created() {
    let socket = io(`${location.origin}`);

    socket.on('connect', function () {
      socket.emit('join_room');
      // TODO:
      this.connect()
    });
    setInterval(function () {
      if (this.connected) {
        socket.emit('status', {message: 'Отправка задач пользователя и обновление статуса'});
      }
    }, 1000);

    socket.on('tasks', function (data) {
      console.log(data.tasks_user);
    });
  },
  beforeCreate() {
    this.$store.commit('initialiseStore');
  }
}
</script>