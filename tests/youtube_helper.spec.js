describe('YouTube helper', () => {
    it('Parses YouTube URL', () => {
        let tests = {
            'kxGWsHYITAw': 'kxGWsHYITAw',
            'https://www.youtube.com/watch?v=v3fOFLXgCbo': 'v3fOFLXgCbo',
            'https://www.youtube.com/watch?v=kxGWsHYITAw': 'kxGWsHYITAw',
            'http://youtu.be/kxGWsHYITAw': 'kxGWsHYITAw',
            'https://youtu.be/v3fOFLXgCbo': 'v3fOFLXgCbo',
            'http://youtu.be/afa-5HQHiAs': 'afa-5HQHiAs',
            'https://www.youtube.com/watch?feature=feedrec_grec_index&v=0zM3nApSvMg': '0zM3nApSvMg',
            'youtube.com/watch?list=FLUHLtib2BztRazu-YgGRXRA&v=sZsJyCyGBSI&index=3&t=0s': 'sZsJyCyGBSI',
            '//www.youtube-nocookie.com/embed/up_lNV-yoK4?rel=0': 'up_lNV-yoK4',
            'http://www.youtube.com/user/Scobleizer#p/u/1/1p3vcRhsYGo': '1p3vcRhsYGo',
            'http://www.youtube.com/watch?v=cKZDdG9FTKY&feature=channel': 'cKZDdG9FTKY',
            'http://www.youtube.com/watch?v=yZ-K7nCVnBI&playnext_from=TL&videos=osPknwzXEas&feature=sub': 'yZ-K7nCVnBI',
            'http://www.youtube.com/ytscreeningroom?v=NRHVzbJVx8I': 'NRHVzbJVx8I',
            'http://www.youtube.com/user/SilkRoadTheatre#p/a/u/2/6dwqZw0j_jY': '6dwqZw0j_jY',
            'http://www.youtube.com/watch?v=6dwqZw0j_jY&feature=youtu.be': '6dwqZw0j_jY',
            'http://www.youtube.com/user/Scobleizer#p/u/1/1p3vcRhsYGo?rel=0': '1p3vcRhsYGo',
            'http://www.youtube.com/embed/nas1rJpm7wY?rel=0': 'nas1rJpm7wY',
            'http://www.youtube.com/watch?v=peFZbP64dsU': 'peFZbP64dsU',
            'http://youtube.com/v/dQw4w9WgXcQ?feature=youtube_gdata_player': 'dQw4w9WgXcQ',
            'http://youtube.com/vi/dQw4w9WgXcQ?feature=youtube_gdata_player': 'dQw4w9WgXcQ',
            'http://youtube.com/?v=dQw4w9WgXcQ&feature=youtube_gdata_player': 'dQw4w9WgXcQ',
            'http://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtube_gdata_player': 'dQw4w9WgXcQ',
            'http://youtube.com/?vi=dQw4w9WgXcQ&feature=youtube_gdata_player': 'dQw4w9WgXcQ',
            'http://youtube.com/watch?v=dQw4w9WgXcQ&feature=youtube_gdata_player': 'dQw4w9WgXcQ',
            'http://youtube.com/watch?vi=dQw4w9WgXcQ&feature=youtube_gdata_player': 'dQw4w9WgXcQ',
            'http://youtu.be/dQw4w9WgXcQ?feature=youtube_gdata_player': 'dQw4w9WgXcQ'
        };

        for (let input in tests) {
            let expected = tests[input];
            expect(getYouTubeId(input)).toEqual(expected, input);
        }
    });
});
