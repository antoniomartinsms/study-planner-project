const { createApp, ref } = Vue

createApp({
  components: {
    AppPageNote
  },
  setup() {
    const email = ref('')
    const password = ref('')
    const loginLoading = ref(false)
    const errorMessage = ref('')
    const tokenReceived = ref(false)

    async function login() {
      const trimmedEmail = email.value.trim()

      errorMessage.value = ''
      tokenReceived.value = false

      if (trimmedEmail === '' || password.value === '') {
        errorMessage.value = 'Preencha email e senha.'
        return
      }

      loginLoading.value = true

      try {
        const response = await api.post('/auth/login', {
          email: trimmedEmail,
          password: password.value
        })

        Auth.saveToken(response.data.access_token)
        tokenReceived.value = true
        location.href = '../index.html'
      } catch (error) {
        errorMessage.value = 'Nao foi possível fazer login.'
        console.error(error)
      } finally {
        loginLoading.value = false
      }
    }

    return {
      email,
      password,
      loginLoading,
      errorMessage,
      tokenReceived,
      login
    }
  }
}).mount('#app')
