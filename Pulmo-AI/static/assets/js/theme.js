window.addEventListener('DOMContentLoaded', function () {
  themeSwitch.addEventListener('change', function () {
    const storedTheme = localStorage.getItem('selectedTheme')
    const currentRoute = window.location.pathname
    fetch(currentRoute, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ theme: storedTheme }),
    })
    // location.href = location.href; 
    console.log(storedTheme)
    location.reload()
  })
})

