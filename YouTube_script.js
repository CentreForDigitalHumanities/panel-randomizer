	/*
		scales video to screensize
		starts video
		prevents video from pausing
		redirects to next group when video has ended
		works on urls:
		https://www.youtube.com/watch?v=kxGWsHYITAw
		https://youtu.be/kxGWsHYITAw
		kxGWsHYITAw
	*/

function youtube_parser(url) {
	var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/;
	var match = url.match(regExp);
	return (match && match[7].length == 11) ? match[7] : false;
}

var video;
var url = document.getElementsByClassName('single-play-video')[0].getAttribute('data-video-url');
if (url.length == 11) {
	video = url;
}
else {
	video = youtube_parser(url);
}

var tag = document.createElement('script');
var screen_width = window.innerWidth;
var video_width;
var video_height;
if (screen_width < 640) {
	video_width = screen_width - (screen_width / 15);
	video_height = (video_width / 16) * 9;
}
else {
	video_width = 640;
	video_height = 390;
}

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];

firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
	player = new YT.Player('video_player', {
		height: video_height,
		width: video_width,
		videoId: video,
		events: {
			'onReady': onPlayerReady,
			'onStateChange': onPlayerStateChange,
			'onError': onPlayerError
		},
		// hide video controls
		playerVars: {
			'controls': 0,
			'disablekb': 1,
			'modestbranding': 1,
			'showinfo': 0,
			'fs': 0,
			'showsearch': 0,
		}

	});
}


function onPlayerError(event) {
	alert('Video does not play, please contact research department')

}


function onPlayerReady(event) {
	event.target.playVideo();
}


function onPlayerStateChange(event) {
	if (event.data == YT.PlayerState.PAUSED) {
		event.target.playVideo(); //disable pausing the video, by starting it again
	}

	if (event.data == YT.PlayerState.ENDED) {
		document.getElementById("ls-button-submit").click(); //click the 'next' button in Lime Survey
	}
}
