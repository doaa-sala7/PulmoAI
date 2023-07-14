const themeSwitch = document.getElementById('theme-switch')

window.addEventListener('DOMContentLoaded', function () {
  themeSwitch.addEventListener('change', function () {
    if (this.checked) {
      storeTheme('dark')
      applyTheme('dark')
    } else {
      storeTheme('light')
      applyTheme('light')
    }
  })
})
function goBack() {
  window.history.back();
}

// Function to store the selected theme
function storeTheme(theme) {
  localStorage.setItem('selectedTheme', theme)
}

// Function to apply the selected theme
function applyTheme(theme) {
  document.querySelector('html').setAttribute('data-theme', theme)
}

// Retrieve the stored theme and apply it on page load
const storedTheme = localStorage.getItem('selectedTheme')
if (storedTheme === 'dark') {
  themeSwitch.checked = true
  applyTheme('dark')
} else {
  themeSwitch.checked = false
  applyTheme('light')
}
