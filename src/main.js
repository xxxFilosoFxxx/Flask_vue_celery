import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
// import SocketIO from 'socket.io-client'
// import VueSocketIO from 'vue-3-socket.io'
import { Quasar } from 'quasar'
import quasarUserOptions from './quasar-user-options'

createApp(App).use(Quasar, quasarUserOptions)
    .use(router)
    .use(store)
    // .use(new VueSocketIO({
    //     debug: true,
    //     connection: SocketIO(`${location.origin}`),
    //     vuex: {
    //       store,
    //       actionPrefix: "SOCKET_",
    //       mutationPrefix: "SOCKET_"
    //     }
    // }))
    .mount('#app');