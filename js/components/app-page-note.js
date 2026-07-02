const AppPageNote = {
  props: {
    title: {
      type: String,
      required: true
    }
  },
  template: `
    <header class="page-note">
      <h1 class="page-note-title">{{ title }}</h1>
      <p class="page-note-text">Base simples para começar uma pagina do projeto.</p>
    </header>
  `
}
