import { createStore } from 'vuex'
import axios from 'axios'
import router from '../router'

const task = {
    id: null,
    msisdn: null,
    radius: null,
    delta: null,
    status: null
}

export default createStore({
    state: {
        currentTask: task,
        tasksList: [],
        allTasksList: [],
        username: ''
    },
    mutations: {
        initialiseStore(state) {
            if (localStorage.getItem('success_login')) {
                state.username = localStorage.getItem('success_login');
            }
            if (JSON.parse(localStorage.getItem('tasks'))) {
                state.allTasksList = JSON.parse(localStorage.getItem('tasks'));
            }
            if (JSON.parse(localStorage.getItem('status'))) {
                state.tasksList = JSON.parse(localStorage.getItem('status'));
            }
        },
        resetState(state) {
            state.currentTask = task;
            state.tasksList = [];
            state.allTasksList = [];
            state.username = '';
            localStorage.removeItem('success_login');
            localStorage.removeItem('tasks');
            localStorage.removeItem('status');
        },
        setCurrentTask(state, value) {
            state.currentTask.id = value['task_id'];
            if (value['task_result'] !== null) {
                state.currentTask.msisdn = value['task_result'].msisdn;
                state.currentTask.radius = value['task_result'].radius;
                state.currentTask.delta = value['task_result'].delta;
            }
            state.currentTask.status = value['state'];
        },
        setTasksList(state, value) {
            localStorage.setItem('status', JSON.stringify(value));
            state.tasksList = value;
        },
        setAllTasksList(state, value) {
            localStorage.setItem('tasks', JSON.stringify(value));
            state.allTasksList = value;
        },
        setUsername(state, value) {
            localStorage.setItem('success_login', value);
            state.username = value;
        },
        clearTasksList(state) {
            state.tasksList = []
        }
    },
    actions: {
        sendTask(context, task_json) {
            axios.post('/api/send_task', task_json)
                .then((response) => {
                    let task = {id: response.data['task_id'], status: response.data.status};
                    console.log(task);
                })
                .catch(function () {
                    alert('Ошибка при отправке задачи в очередь');
                });
        },
        getTask(context, urlTask) {
            axios.get('/result_task/' + urlTask)
                .then((response) => {
                    context.commit('setCurrentTask', response.data);
                    router.push({ path: `/status/${urlTask}`});
                })
                .catch(function () {
                    alert('Ошибка при загрузке задачи');
                });
        },
        getTasks(context) {
            axios.get('/all_result_tasks')
                .then((response) => {
                    context.commit('setAllTasksList', response.data);
                })
                .catch(function () {
                    alert('Ошибка при загрузке задач');
                });
        },
        loadTasks(context) {
            axios.get('/status_tasks')
                .then((response) => {
                    context.commit('setTasksList', response.data['tasks']);
                })
                .catch(function () {
                    alert('Ошибка при загрузке статуса задач');
                });
        },
        sendLogin(context, login_json) {
            axios.post('/api/login', login_json)
                .then((response) => {
                    alert(response.data.message);
                    context.commit('setUsername', response.data.username);
                    router.push(response.data.path);
                })
                .catch(function () {
                    alert('Ошибка при входе пользователя');
                });
        },
        sendRegister(context, register_json) {
            axios.post('/api/register', register_json)
                .then((response) => {
                    alert(response.data.message);
                    router.push(response.data.path);
                })
                .catch(function () {
                    alert('Ошибка при регистрации пользователя');
                });
        },
        onLogout(context) {
            axios.get('/logout')
                .then((response) => {
                    context.commit('resetState');
                    alert(response.data.message);
                    router.push(response.data.path);
                })
                .catch(function () {
                    alert('Ошибка при выходе пользователя');
                });
        }
    },
    modules: {
    }
})