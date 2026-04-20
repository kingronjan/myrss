import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// Enable dark mode
const darkMediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
function toggleDarkMode(isDark: boolean) {
  if (isDark) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// Initial check
toggleDarkMode(darkMediaQuery.matches)

// Watch for changes
darkMediaQuery.addEventListener('change', (e) => toggleDarkMode(e.matches))

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')
