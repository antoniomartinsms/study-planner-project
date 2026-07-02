const { createApp, onMounted, ref } = Vue

createApp({
  components: {
    AppPageNote
  },
  setup() {
    const isLoggedIn = ref(Auth.isLoggedIn())
    const loading = ref(isLoggedIn.value)
    const errorMessage = ref('')
    const user = ref(null)

    async function fetchCurrentUser() {
      if (!isLoggedIn.value) {
        user.value = null
        return
      }

      loading.value = true
      errorMessage.value = ''

      try {
        const response = await api.get('/users/me')
        user.value = response.data
      } catch (error) {
        Auth.logout()
        isLoggedIn.value = false
        user.value = null
        errorMessage.value = 'Sua sessão expirou ou o token e inválido.'
        console.error(error)
      } finally {
        loading.value = false
      }
    }

    function formatDate(date) {
      if (!date) {
        return '-'
      }

      return new Date(date).toLocaleString('pt-BR')
    }

    function logout() {
      Auth.logout()
      isLoggedIn.value = false
      user.value = null
    }

    onMounted(() => {
      fetchCurrentUser()
    })

    return {
      isLoggedIn,
      loading,
      errorMessage,
      user,
      formatDate,
      logout
    }
  }
}).mount('#app')
