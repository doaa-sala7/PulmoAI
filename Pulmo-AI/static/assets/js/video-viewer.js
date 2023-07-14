const videoPlayer = document.getElementById('videoPlayer')
const playPauseBtn = document.getElementById('playPauseBtn')
const goBackBtn = document.getElementById('goBackBtn')

playPauseBtn.addEventListener('click', togglePlayPause)
goBackBtn.addEventListener('click', goBack)

function togglePlayPause() {
  if (videoPlayer.paused || videoPlayer.ended) {
    videoPlayer.play()
    playPauseBtn.textContent = 'Pause'
  } else {
    videoPlayer.pause()
    playPauseBtn.textContent = 'Play'
  }
}

function goBack() {
  videoPlayer.currentTime -= 5 // Go back 5 seconds
}
