document.addEventListener('DOMContentLoaded', function () {
  const fileInput = document.getElementById('file-input')
  const selectedImage = document.getElementById('selected-image')
  const placeholderText = document.getElementById('placeholder-text')

  fileInput.addEventListener('change', function () {
    const file = fileInput.files[0]

    if (file) {
      const imageUrl = URL.createObjectURL(file)

      selectedImage.onload = function () {
        URL.revokeObjectURL(this.src)
      }

      selectedImage.src = imageUrl
      selectedImage.style.display = 'block'
      placeholderText.style.display = 'none'
    } else {
      selectedImage.src = ''
      selectedImage.style.display = 'none'
      placeholderText.style.display = 'block'
    }
  })
})
