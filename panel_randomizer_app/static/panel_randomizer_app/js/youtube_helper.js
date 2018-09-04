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
	
	Optionally:

	Add data-before-next to make it appear and play *before*
	continuing to the next question. This is a work-around for Safari
	which doesn't allow auto-playing videos anymore.

	E.g.

	<div class="single-play-video" data-video-url="URL" data-before-next="true"></div>
*/

var YT; // set by YouTube iframe

(function () {
	var ClassName = 'single-play-video';
	var YouTubeIdPattern = /^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*/;

	function getYouTubeId(url) {
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

	var tag = document.createElement('script');
	tag.src = "https://www.youtube.com/iframe_api";
	var firstScriptTag = document.getElementsByTagName('script')[0];

	firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

	window['onYouTubeIframeAPIReady'] = function () {
		bindSinglePlay(document.getElementsByClassName(ClassName));
	}

	function bindSinglePlay(elements) {
		for (var i = 0; i < elements.length; i++) {
			createPlayer(elements[i]);
		}
	}

	function createPlayer(element) {
		var beforeNext = !!element.getAttribute('data-before-next');

		var dimensions = getVideoDimensions(beforeNext);
		var videoWidth = dimensions[0];
		var videoHeight = dimensions[1];

		var url = element.getAttribute('data-video-url');
		var videoId = getYouTubeId(url);

		if (beforeNext) {
			// already load the video player and hide it
			// this will be shown when the user clicks the 'next'-button
			videoElement = document.createElement('div');

			element.appendChild(videoElement);
			element.style.height = '0';
			element.style.overflow = 'hidden';
		} else {
			videoElement = element;
		}

		var player = new YT.Player(videoElement, {
			height: videoHeight,
			width: videoWidth,
			videoId: videoId,
			events: {
				'onReady': !beforeNext ? onPlayerReady : function () {},
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

		if (beforeNext) {
			wrapNextButton(element, player);
		}
	}

	/**
	 * Limits the size of the video
	 */
	function getVideoDimensions(beforeNext) {
		var screenWidth = window.innerWidth;
		var screenHeight = window.innerHeight;

		var videoWidth, videoHeight;

		if (beforeNext) {
			// this is played in a box in the entire window.
			// Can make it quite big
			videoWidth = screenWidth - 20;
			videoHeight = (videoWidth / 16) * 9;

			if (videoHeight > (screenHeight - 20)) {
				videoHeight = screenHeight - 20;
				videoWidth = (screenHeight / 9) * 16;
			}
		} else {
			// should fit inside the question box
			if (screenWidth < 640) {
				videoWidth = screenWidth - (screenWidth / 5);
				videoHeight = (videoWidth / 16) * 9;
			} else {
				videoWidth = 640;
				videoHeight = 390;
			}
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
			goNext();
			event.target.destroy();
		}
	}

	function getNextButton() {
		// click the 'next' button in LimeSurvey. 
		// Different versions of LimeSurvey provide different IDs
		var nextButton = document.getElementById("ls-button-submit"); // LimeSurvey 3.12

		if (nextButton == null) {
			nextButton = document.getElementById("movenextbtn"); // LimeSurvey 2.5
		}

		return nextButton;
	}

	function goNext() {
		var nextButton = getNextButton();
		// LimeSurvey disables this button on click, re-enable it
		// to allow the click event to work.		
		nextButton.className = nextButton.className.replace('disabled', '');
		nextButton.disabled = false;
		nextButton.click();
	}

	function wrapNextButton(container, player) {
		var nextButton = getNextButton();
		nextButton.style.display = 'none';

		var fakeButton = document.createElement(nextButton.tagName);
		fakeButton.className = nextButton.className.replace('submit', '');
		fakeButton.innerHTML = nextButton.innerHTML;

		nextButton.parentNode.appendChild(fakeButton);

		fakeButton.addEventListener('click', function (event) {
			if (!checkMandatoryQuestions()) {
				// actually submit, when the check for mandatory answers
				// fails: the validation errors are rendered on the server
				goNext();
				return;
			}

			container.style.position = 'fixed';
			container.style.height = 'auto';
			container.style.overflow = 'inherit';
			container.style.top = 0;
			container.style.left = 0;
			container.style.width = '100%';
			container.style.height = '100%';
			container.style.background = 'black';
			container.style.textAlign = 'center';
			container.style.zIndex = 2000;

			event.preventDefault();
			player.playVideo();
		});
	}

	function checkMandatoryQuestions() {
		var mandatoryQuestions = document.getElementsByClassName('mandatory');
		for (var i = 0; i < mandatoryQuestions.length; i++) {
			var question = mandatoryQuestions[i];
			var checked = false;
			var radios = question.getElementsByClassName('radio');
			if (radios.length) {
				for (var j = 0; j < radios.length; j++) {
					if (radios[j].checked) {
						checked = true;
					}
				}
			}

			var fields = question.querySelectorAll('.textarea,.numeric');
			if (fields.length) {
				for (var j = 0; j < fields.length; j++) {
					if (fields[j].value) {
						checked = true;
					}
				}
			}
			if (!checked) {
				return false;
			}
		}

		return true;
	}
})();