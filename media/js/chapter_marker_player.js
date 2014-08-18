/*
 Copyright 2012 Google Inc. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 */

jQuery(videoInit);

function videoInit () {
/*

Part 1
<iframe width="560" height="315" src="http://www.youtube.com/embed/?rel=0" frameborder="0" allowfullscreen></iframe>

Part 2
<iframe width="560" height="315" src="http://www.youtube.com/embed/?rel=0" frameborder="0" allowfullscreen></iframe>
*/
    var videoOneId = 'APsV5aFubCM';
    var videoTwoId = 'M1UKzxYJUJY';

    if (jQuery ('#video_1_container').length > 0) {
        window.ChapterMarkerPlayer.insert({
            container: 'video_1_container',
            playerOptions : {'playerVars': {'rel': 0}},
            videoId: videoOneId,
            width: 600,
            chapters: {
                0: 'Title Slide',
                31: 'Direct Acting Antivirals',
                89: 'Minimum to know pre-treatment',
                132: 'IDSA and AASID guidelines',
                165: 'Part 1: HCV G2 and G3 treatment',
                174: 'Genotype 2 SVR data',
                223: 'Genotype 2 SRV data for cirrhotic patients',
                279: 'Genotype 3 SVR data',
                352: 'Genotype 3 SVR data for cirrhotic patients',
                414: 'No role for response guided therapy',
                484: 'Safety',
                518: 'Sofosbuvir and drug interactions',
                565: 'Sofosbuvir and HIV Medications'
            }
        });
    }

    if (jQuery ('#video_2_container').length > 0) {
        window.ChapterMarkerPlayer.insert({
            container: 'video_2_container',
            playerOptions : {'playerVars': {'rel': 0}},
            videoId: videoTwoId,
            width: 600,
            chapters: {
                0: 'Title Slide',
                10: 'HIV G1 treatment evolution',
                36: 'Genotype 1 SVR data',
                84: 'Predictors of failure',
                125: 'Safety',
                159: 'Definition of IFN ineligible',
                184: 'G1 IFN Free DAA data',
                302: 'Virologic Failure=Relapse',
                330: 'Adverse events and dose modifications',
                345: 'SVR rates in patients with cirrhosis',
                396: 'Other factors that affect response',
                434: 'Simeprevir and drug interactions',
                462: 'Simeprevir and HIV medications'
            }
        });
    }
}

// BEGIN_INCLUDE(namespace)
window.ChapterMarkerPlayer = {
  // Inserts a new YouTube iframe player and chapter markers as a child of an
  // existing HTML element on a page.
    insert: function(params) {
// END_INCLUDE(namespace)
    // We need to reserve 30px for the player's control bar when automatically sizing the player.
        var YOUTUBE_CONTROLS_HEIGHT = 30;
    // Assume a 9:16 (width:height) ratio when we need to calculate a player's height.
        var PLAYER_HEIGHT_TO_WIDTH_RATIO = 9 / 16;
        var DEFAULT_PLAYER_WIDTH = 400;
// BEGIN_INCLUDE(validation1)
    // params contains the following required and optional parameter names and values:
    //   videoId: (required) The YouTube video id of the video to be embedded.
    //   chapters: (required) Mapping of times (seconds since the video's start) to chapter titles.
    //   width: (optional) The width of the embedded player. 400px is used by default.
    //   playerOptions: (optional) An object corresponding to the options that can be passed to the
    //                  YT.Player constructor. See https://developers.google.com/youtube/iframe_api_reference#Loading_a_Video_Player

        if (!('videoId' in params)) {
            throw ('The "videoId" parameter must be set to ' +
                   'the YouTube video id to be embedded.');
        }

        if (!('chapters' in params)) {
            throw ('The "chapters" parameter must be set to ' +
                   'the mapping of times to chapter titles.');
        }
// END_INCLUDE(validation1)
// BEGIN_INCLUDE(time_sort)
        var times = [];
        for (var time in params.chapters) {
            if (params.chapters.hasOwnProperty(time)) {
                times.push(time);
            }
        }
    // Sort the times numerically for display purposes.
    // See https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Array/sort#Examples
        times.sort(function(a, b) {
            return a - b;
        });
// END_INCLUDE(time_sort)
        var width = params.width || DEFAULT_PLAYER_WIDTH;

        if ('YT' in window && 'Player' in window.YT) {
      // If the iframe player API is already available, proceed to loading the player using the API.
            insertPlayerAndAddChapterMarkers(params);
        } else {
      // Load the API, and add a callback to the queue to load the player once the API is available.
            if (!('onYouTubePlayerAPIReady' in window)) {
// BEGIN_INCLUDE(invoke_callbacks)
                var cmp = window.ChapterMarkerPlayer;
                window.onYouTubePlayerAPIReady = function() {
                    for (var i = 0;
                         i < cmp.onYouTubePlayerAPIReadyCallbacks.length;
                         i++) {
                        cmp.onYouTubePlayerAPIReadyCallbacks[i]();
                    }
                };
// END_INCLUDE(invoke_callbacks)
// BEGIN_INCLUDE(load_api)
        // Dynamic <script> tag insertion will effectively load the iframe Player API on demand.
        // We only want to do this once, so it's protected by the
        // !('onYouTubePlayerAPIReady' in window) check.
                var scriptTag = document.createElement('script');
        // This scheme-relative URL will use HTTPS if the host page is accessed via HTTPS,
        // and HTTP otherwise.
                scriptTag.src = '//www.youtube.com/player_api';
                var firstScriptTag = document.getElementsByTagName(
                        'script')[0];
                firstScriptTag.parentNode.insertBefore(
                         scriptTag, firstScriptTag);
// END_INCLUDE(load_api)
            }
// BEGIN_INCLUDE(queue_callbacks)
      // We need to handle the situation where multiple ChapterMarkerPlayer.insert() calls are made
      // before the YT.Player API is loaded. We do this by maintaining an array of functions, each
      // of which adds a specific player and chapters. The functions will be executed when
      // onYouTubePlayerAPIReady() is invoked by the YT.Player API.
            window.ChapterMarkerPlayer.onYouTubePlayerAPIReadyCallbacks.push(
                function() {
                    insertPlayerAndAddChapterMarkers(params);
                });
// END_INCLUDE(queue_callbacks)
        }

// BEGIN_INCLUDE(load_player)
    // Calls the YT.Player constructor with the appropriate options to add the iframe player
    // instance to a parent element.
    // This is a private method that isn't exposed via the ChapterMarkerPlayer namespace.
        function initializePlayer(containerElement, params) {
      //console.log ('params is');
      //console.log (params);

            var playerContainer = document.createElement('div');
            containerElement.appendChild(playerContainer);

      // Attempt to use any custom player options that were passed in via params.playerOptions.
      // Fall back to reasonable defaults as needed.
            var playerOptions = params.playerOptions || {};
      //console.log ('playerOptions.playerVars are');
      //console.log (playerOptions.playerVars);
            return new YT.Player(playerContainer, {
        // Maintain a 16:9 aspect ratio for the player based on the width passed in via params.
        // Override can be done via params.playerOptions if needed
                height: playerOptions.height ||
                width * PLAYER_HEIGHT_TO_WIDTH_RATIO + YOUTUBE_CONTROLS_HEIGHT,
                width: playerOptions.width || width,
        // Unless playerVars are explicitly provided, use a reasonable default of { autohide: 1 },
        // which hides the controls when the mouse isn't over the player.
                playerVars: playerOptions.playerVars || {autohide: 1},
                videoId: params.videoId,
                events: {
                    onReady: playerOptions.onReady,
                    onStateChange: playerOptions.onStateChange,
                    onPlaybackQualityChange:
                       playerOptions.onPlaybackQualityChange,
                    onError: playerOptions.onError
                }
            });
        }

// END_INCLUDE(load_player)

// BEGIN_INCLUDE(format_timestamp)
    // Takes a number of seconds and returns a #h##m##s string.
        function formatTimestamp(timestamp) {
            var hours = Math.floor(timestamp / 3600);
            var minutes = Math.floor((timestamp - (hours * 3600)) / 60);
            var seconds = timestamp % 60;

            var formattedTimestamp = (seconds < 10 ? '0' : '') +
								seconds + 's';
            if (minutes > 0) {
                formattedTimestamp = (minutes < 10 ? '0' : '') +
                    minutes + 'm' + formattedTimestamp;
            }
            if (hours > 0) {
                formattedTimestamp = hours + 'h' + formattedTimestamp;
            }

            return formattedTimestamp;
        }

// END_INCLUDE(format_timestamp)

// BEGIN_INCLUDE(add_chapter_markers)
    // Adds a sorted list of chapters below the player. Each chapter has an onclick handler that
    // calls the iframe player API to seek to a specific timestamp in the video.
    // This is a private method that isn't exposed via the ChapterMarkerPlayer namespace.
        function addChapterMarkers(containerElement, player) {
            var ol = document.createElement('ol');
            ol.setAttribute('class', 'chapter-list');
            ol.setAttribute('style', 'width: ' + width + 'px');
            containerElement.appendChild(ol);

            var clickfunc = function() {
                // 'this' will refer to the element that was clicked.
                player.seekTo(this.getAttribute('data-time'));
            };
            for (var i = 0; i < times.length; i++) {
                var time = times[i];
                var chapterTitle = params.chapters[time];

                var li = document.createElement('li');
                li.setAttribute('data-time', time);
                li.textContent = formatTimestamp(time) + ': ' + chapterTitle;
                li.onclick = clickfunc;
                ol.appendChild(li);
            }
        }

// END_INCLUDE(add_chapter_markers)

    // Convenience method to call both initializePlayer and addChapterMarkers.
    // This is a private method that isn't exposed via the ChapterMarkerPlayer namespace.
        function insertPlayerAndAddChapterMarkers(params) {
// BEGIN_INCLUDE(validation2)
            var containerElement = document.getElementById(params.container);
            if (!containerElement) {
                throw ('The "container" parameter must be set ' +
                       'to the id of a existing HTML element.');
            }
// END_INCLUDE(validation2)

            var player = initializePlayer(containerElement, params);
            addChapterMarkers(containerElement, player);
        }
    },
// BEGIN_INCLUDE(callback_array)
  // This is used to keep track of the callback functions that need to be invoked when the iframe
  // API has been loaded. It avoids a race condition that would lead to issues if multiple
  // ChapterMarkerPlayer.insert() calls are made before the API is available.
    onYouTubePlayerAPIReadyCallbacks: []
// END_INCLUDE(callback_array)
};
