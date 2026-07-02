# Frontend Template

Template simples com HTML estático, Vue 3 por CDN e JavaScript separado por página.

## Estrutura

- `index.html`: página inicial do template
- `pages/login.html`: exemplo de formulário de login
- `js/api.js`: instância do Axios e configuração da `API_URL`
- `js/auth.js`: armazenamento e remoção do token JWT
- `js/index.js`: lógica da página inicial
- `js/login.js`: lógica da página de login
- `js/components/app-page-note.js`: componente simples de exemplo com `props`
- `style.css`: CSS base reutilizável

## Configurando a API

Edite `js/api.js` e ajuste a constante:

```js
const API_URL = 'http://localhost:5000'
```

## Fluxo de autenticação

1. A página `pages/login.html` envia `email` e `password` para `POST /auth/login`
2. O token retornado é salvo no `localStorage`
3. A `index.html` verifica se existe token
4. Quando há token, a página chama `GET /users/me` para mostrar os dados do usuário autenticado

## Como criar novas páginas

1. Crie um novo arquivo em `pages/`
2. Reaproveite `../style.css`
3. Importe `../js/auth.js` e `../js/api.js` quando a página precisar falar com a API
4. Se quiser seguir o exemplo do template, reaproveite o componente `app-page-note`
