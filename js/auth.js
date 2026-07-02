function saveToken(token) {
  localStorage.setItem('authToken', token)
  applyToken()
}

function getToken() {
  return localStorage.getItem('authToken') || ''
}

function isLoggedIn() {
  return getToken() !== ''
}

function getAuthorizationHeader() {
  const token = getToken()

  if (!token) {
    return {}
  }

  return {
    Authorization: `Bearer ${token}`
  }
}

function logout() {
  localStorage.removeItem('authToken')
  applyToken()
}

const Auth = {
  saveToken,
  getToken,
  isLoggedIn,
  getAuthorizationHeader,
  logout
}

applyToken()