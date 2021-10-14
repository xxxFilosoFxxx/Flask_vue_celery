<template>
  <div class="q-pa-md" style="max-width: 400px">
    <q-form
        @submit.prevent="submitLogin()"
        @reset="onReset()"
        class="q-gutter-md">
      <q-input outlined
               v-model="login"
               label="Логин"
               lazy-rules
               :rules="[
                  val => val && val.length > 0 || 'Введите логин'
                ]"/>
      <q-input outlined
               :type="isPwd ? 'password' : 'text'"
               v-model="password"
               label="Пароль"
               lazy-rules
               :rules="[
                  val => val && val.length > 0 || 'Введите пароль'
               ]">
        <template v-slot:append>
          <q-icon
              :name="isPwd ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="isPwd = !isPwd"
          />
        </template>
      </q-input>

      <div>
        <q-btn type="submit" label="Отправить" color="indigo-10" />
        <q-btn type="reset" label="Сбросить" color="primary" flat class="q-ml-sm" />
      </div>
      <div>
        <q-btn color="primary" label="Регистрация" to="/register" />
      </div>
    </q-form>

  </div>
</template>

<script>
import { ref } from "vue";

export default {
  name: "LoginForm",
  data() {
    return {
      login: ref(null),
      password: ref(null),
      isPwd: ref(true)
    }
  },
  methods: {
    submitLogin() {
      let login_json = {login: this.login, password: this.password};
      this.$store.dispatch('sendLogin', login_json);
    },
    onReset() {
      this.login = null;
      this.password = null;
    }
  }
}
</script>

<style scoped>

</style>