/*
	Embeds a video on a LimeSurvey page.
	* scales video to screensize,
	* starts the video;
	* prevents video from pausing
	* redirects to the next group when video has ended
	
	Usage:

	Add the following in the question:
	
	<div class="single-play-video" data-video-url="URL"></div>

	Replace it with a YouTube URL or ID.

	Works on urls:
	https://www.youtube.com/watch?v=kxGWsHYITAw
	https://youtu.be/kxGWsHYITAw
	kxGWsHYITAw
*/
const ClassName = 'single-play-video';
const YouTubeIdPattern = /^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*/;
export function getYouTubeId(url) {
	var match = url.match(YouTubeIdPattern);
	if (match && match[1]) {
		return match[1];
	}

	if (url.length >= 11 && /^[^#\&\?]*$/.test(url)) {
		// only an ID
		return url;
	}
	return false;
}

declare let YT; // set by YouTube iframe
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];

firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

window['onYouTubeIframeAPIReady'] = function () {
	bindSinglePlay(document.getElementsByClassName(ClassName));
}

function bindSinglePlay(elements) {
	let [videoWidth, videoHeight] = getVideoDimensions();

	for (let element of elements) {
		var url = element.getAttribute('data-video-url');
		var videoId = getYouTubeId(url);

		new YT.Player(element, {
			height: videoHeight,
			width: videoWidth,
			videoId: videoId,
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
				'rel': 0
			}
		});
	}
}

/**
 * Limits the size of the video to 640x390
 */
function getVideoDimensions() {
	var screenWidth = window.innerWidth;
	var videoWidth, videoHeight;
	if (screenWidth < 640) {
		videoWidth = screenWidth - (screenWidth / 15);
		videoHeight = (videoWidth / 16) * 9;
	}
	else {
		videoWidth = 640;
		videoHeight = 390;
	}

	return [videoWidth, videoHeight];
}

function onPlayerError(event) {
	alert('Video does not play, please contact research department')
}

function onPlayerReady(event) {
	event.target.playVideo();
}

function onPlayerStateChange(event) {
	if (event.data == YT.PlayerState.PAUSED) {
		// disable pausing the video, by starting it again
		event.target.playVideo();
	}

	if (event.data == YT.PlayerState.ENDED) {
		// click the 'next' button in Lime Survey
		document.getElementById("ls-button-submit").click();
		event.target.destroy();
	}
}
