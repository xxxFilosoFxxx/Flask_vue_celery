import { createRouter, createWebHistory } from 'vue-router';
import store from '../store/index';
import AllTasks from "../views/AllTasks.vue";
import Task from "../views/Task.vue";
import Home from "../views/Home.vue";

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {requiresAuth: true},
  },
  {
    path: '/all_tasks',
    name: 'AllTasks',
    component: AllTasks,
    meta: {requiresAuth: true},
  },
  {
    path: '/status/:uuid',
    name: 'Task',
    component: Task,
    meta: {requiresAuth: true}
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import("../views/Login.vue")
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import("../views/Register.vue")
  },
  {
    path: '/:noPage(.*)*',
    name: 'NotFound',
    component: () => import("../views/NotFound.vue")
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.state.username || store.state.username.length === 0) {
      next({
        name: 'Login',
        query: {redirect: to.fullPath}
      });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
