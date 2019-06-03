/*
    Embeds a video on a LimeSurvey page.
    * scales video to screensize,
    * starts the video;
    * prevents video from pausing
    * redirects to the next group when video has ended

    Usage:
    Add the following in the question:

    <div class="single-play-video" data-video-url="URL"></div>
    Replace it with a YouTube/Vimeo URL or ID.
    Works on urls:
    https://www.youtube.com/watch?v=-9-Te-DPbSE
    https://youtu.be/-9-Te-DPbSE
    https://vimeo.com/44474689
    kxGWsHYITAw
    44474689

    Optionally:

    Add data-before-next to make it appear and play *before*
    continuing to the next question. This is a work-around for Safari
    which doesn't allow auto-playing videos anymore.

    E.g.

    <div class="single-play-video" data-video-url="URL" data-before-next="true"></div>

    Add data-provider to specify the provider (youtube, vimeo).
    Normally this should be auto-detected properly.
*/
(function () {
    var PlyrJs = 'https://cdn.plyr.io/3.5.4/plyr.polyfilled.js',
        PlyrCss = 'https://cdn.plyr.io/3.5.4/plyr.css',
        ClassName = 'single-play-video',
        VimeoPattern = /(vimeo\.com\/|^\d+$)/i,
        YouTubeUrlPattern = /^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*/,
        YouTubeIdPattern = /^[^#\&\?]*$/;

    function getSource(element) {
        var url = element.getAttribute('data-video-url');
        var provider = element.getAttribute('data-provider');
        if (provider == 'vimeo' || !provider && VimeoPattern.test(url)) {
            return {
                provider: 'vimeo',
                videoId: url
            }
        } else if (provider == 'youtube' || !provider &&
            (YouTubeUrlPattern.test(url) || YouTubeIdPattern.test(url))) {
            return {
                provider: 'youtube',
                videoId: getYouTubeId(url)
            }
        }

        throw ({
            message: "Unknown provider",
            element: element,
            url: url,
            provider: provider
        });
    }

    // if it already exists globally, set it: because it could be created during a test
    getYouTubeId = function (url) {
        var match = url.match(YouTubeUrlPattern);
        if (match && match[1]) {
            return match[1];
        }

        if (url.length >= 11 && YouTubeIdPattern.test(url)) {
            // only an ID
            return url;
        }
        return false;
    }

    function load() {
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = PlyrCss;

        var script = document.createElement('script');
        script.onload = onload;
        script.src = PlyrJs;

        var firstScriptTag = document.getElementsByTagName('script')[0];

        firstScriptTag.parentNode.insertBefore(link, firstScriptTag);
        firstScriptTag.parentNode.insertBefore(script, firstScriptTag);
    }

    function onload() {
        bindSinglePlay(document.getElementsByClassName(ClassName));
    }

    function bindSinglePlay(elements) {
        for (var i = 0; i < elements.length; i++) {
            createPlayer(elements[i]);
        }
    }

    function createPlayer(element) {
        // clear any spaces, also allows for a fallback message
        element.innerHTML = '';

        var beforeNext = !!element.getAttribute('data-before-next');
        var dimensions = getVideoDimensions(beforeNext);
        var videoWidth = dimensions[0];
        var videoHeight = dimensions[1];

        var source = getSource(element);
        videoId = source.videoId;
        provider = source.provider;

        // already load the video player and hide it
        // this will be shown when the user clicks the 'next'-button
        videoElement = document.createElement('div');

        element.appendChild(videoElement);
        element.style.height = '0';
        element.style.overflow = 'hidden';

        videoElement.setAttribute('data-plyr-provider', provider);
        videoElement.setAttribute('data-plyr-embed-id', videoId);

        var player = new Plyr(videoElement, {
            height: videoHeight,
            width: videoWidth
        });
        player.on('ready', !beforeNext ?
            function (event) {
                onPlayerReady(event, element)
            } : function () { });
        player.on('error', onPlayerError);
        player.on('statechange', onYouTubePlayerStateChange);
        player.on('ended', onEnded(beforeNext, player, element));
        player.on('pause', keepOnPlaying(player));
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

        // this is played in a box in the entire window.
        // Can make it quite big
        videoWidth = screenWidth - 20;
        videoHeight = (videoWidth / 16) * 9;

        if (videoHeight > (screenHeight - 20)) {
            videoHeight = screenHeight - 20;
            videoWidth = (screenHeight / 9) * 16;
        }

        return [videoWidth, videoHeight];
    }

    function onPlayerError(error) {
        if (/playback ?rate/g.test(error.detail.message)) {
            // workaround for Vimeo error
            return;
        }
        var errorText;
        if (error && error.detail && error.detail.message) {
            errorText = error.detail.message;
        } else {
            errorText = error.toString();
        }
        alert('Video does not play, please contact research department:\n\n' + errorText);
        console.log(error);
    }

    function onPlayerReady(event, container) {
        showVideo(container);
        event.detail.plyr.play();
    }

    function onYouTubePlayerStateChange(event) {
        if (event.detail.code == YT.PlayerState.PAUSED) {
            // disable pausing the video, by starting it again
            event.detail.plyr.play();
        }
    }

    function keepOnPlaying(player) {
        return function () {
            player.play();
        }
    }

    function onEnded(beforeNext, player, element) {
        return function () {
            player.destroy();
            if (beforeNext) {
                goNext();
            } else {
                element.remove();
            }
        }
    }

    function getNextButton() {
        // click the 'next' or 'submit' button in LimeSurvey.
        // Different versions of LimeSurvey provide different IDs
        /* LimeSurvey 3.12 */
        return document.getElementById("ls-button-submit") ||
            /* LimeSurvey 2.5 */
            document.getElementById("movenextbtn") ||
            document.getElementById("movesubmitbtn");
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

        fakeButton.addEventListener('click', function (event) {
            if (!checkMandatoryQuestions()) {
                // actually submit, when the check for mandatory answers
                // fails: the validation errors are rendered on the server
                goNext();
                return;
            }

            showVideo(container);

            event.preventDefault();
            player.play();
        });
        fakeButton.className = nextButton.className.replace('submit', '') + ' fake-button';
        fakeButton.innerHTML = nextButton.innerHTML;

        nextButton.parentNode.appendChild(fakeButton);
    }

    function showVideo(container) {
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

    load();
})();
