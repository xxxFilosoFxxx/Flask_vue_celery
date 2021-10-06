import { createStore } from 'vuex'
import axios from 'axios'
import router from '../router'

// TODO: у каждого пользователя есть id -> по нему определеяем его список задач
// TODO: далее -> при отправке/удалении (и тд) обновляем список задач по uuid (reload -> mounted)
// TODO: параллельно -> обновляем данные в БД

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
        username: ''
    },
    mutations: {
        initialiseStore(state) {
            if (localStorage.getItem('success_login')) {
                state.username = localStorage.getItem('success_login');
            }
        },
        resetState(state) {
            state.currentTask = task;
            state.tasksList = [];
            state.username = '';
            localStorage.removeItem('success_login');
        },
        setCurrentTask(state, value) {
            state.currentTask.id = value.id;
            state.currentTask.status = value.status;
        },
        updateCurrentTask(state, value) {
            state.currentTask.msisdn = value.msisdn;
            state.currentTask.radius = value.radius;
            state.currentTask.delta = value.delta;
        },
        setTasksList(state, value) {
            state.tasksList = value;
        },
        setUsername(state, value) {
            localStorage.setItem('success_login', value);
            state.username = value;
        },
        clearTasksList(state) {
            state.tasksList = []
        },
        // reloadTaskList(state) {}
    },
    actions: {
        sendTask(context, task_json) {
            axios.post('/api/send_task', task_json)
                .then((response) => {
                    let task = {id: response.data['task_id'], status: response.data.status};
                    console.log(task);
                    console.log(task.status);
                    context.commit('setCurrentTask', task);
                })
                .catch(function () {
                    alert('Ошибка при отправке задачи в очередь');
                });
        },
        // TODO: добавить маршрут обработки
        loadTasks(context) {
            axios.get('/load_tasks_status')
                .then((response) => {
                    context.commit('setTasksList', response.data['tasks_status']);
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
                    // context.commit('successLoginUser');
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