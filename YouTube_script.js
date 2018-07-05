<script>
/*
  starts video
  prevents video from pausing
  redirects to next group when video has ended
*/

var video_id='sA0-QXbLnaE'; //fill out the id of the desired video
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: '390',
    width: '640',
    videoId: video_id,
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    },
    playerVars: { 
      'controls': 0, 
      'disablekb':1,
      'showinfo': 0,
      'showsearch':0,
      }
  });
}

function onPlayerError(event){
	alert('Afspelen lukt niet, neem aub contact op met de onderzoekers')
}

function onPlayerReady(event) {
  event.target.playVideo();
}

function onPlayerStateChange(event) {
  if(event.data == YT.PlayerState.PAUSED ){
    event.target.playVideo(); //disable pausing the video, by starting it again
  }
  if (event.data == YT.PlayerState.ENDED ) {
    document.getElementById("ls-button-submit").click(); //clicks the 'next' button in Lime Survey
  }
}

</script>
