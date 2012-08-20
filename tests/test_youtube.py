# this code uses the "gdata" library.
# you have to install that first:
#   pip install gdata

import unittest

import gdata.media
import gdata.geo
import gdata.youtube
import gdata.youtube.service

class YoutubeTest(unittest.TestCase):

    def setUp(self):
        self.username = 'nouvak.kcclass@gmail.com'
        self.password = 'KCClassTest'
        self.youtube_service = gdata.youtube.service.YouTubeService()
        # Turn on HTTPS/SSL access.
        # Note: SSL is not available at this time for uploads.
        self.youtube_service.ssl = False
        # Authenticate using your Google email address and password.
        self.youtube_service.ClientLogin(self.username, self.password)
        self.youtube_service.developer_key = 'AI39si6-qCVmA8KI53Eg3NF5VjnsvKYzsmzD4njj0VFnQDWgh-Iv0X3h_ABBCAwMWDe_G3VzEHGcTrd6eAy9QBPKBb3CDDDXJw'
        self.youtube_service.client_id = 'kcclass-media-publish'

    def tearDown(self):
        pass

    def print_entry_details(self, entry):
        print 'Video title: %s' % entry.media.title.text
        print 'Video published on: %s ' % entry.published.text
        print 'Video description: %s' % entry.media.description.text
        print 'Video category: %s' % entry.media.category[0].text
        print 'Video tags: %s' % entry.media.keywords.text
        print 'Video watch page: %s' % entry.media.player.url
        print 'Video flash player URL: %s' % entry.GetSwfUrl()
        print 'Video duration: %s' % entry.media.duration.seconds
        # non entry.media attributes
        if entry.geo is not None:
            print 'Video geo location: %s' % str(entry.geo.location())
        if entry.statistics is not None:
            print 'Video view count: %s' % entry.statistics.view_count
        if entry.rating is not None:
            print 'Video rating: %s' % entry.rating.average
        # show alternate formats
        if entry.media.content is not None:
            for alternate_format in entry.media.content:
                if 'isDefault' not in alternate_format.extension_attributes:
                    print 'Alternate format: %s | url: %s ' % (alternate_format.type, 
                                                               alternate_format.url)
        # show thumbnails
        if entry.media.thumbnail is not None:
            for thumbnail in entry.media.thumbnail:
                print 'Thumbnail url: %s' % thumbnail.url
            
    def print_video_feed(self, feed):
        for entry in feed.entry:
            self.print_entry_details(entry)

    def test_get_standard_feeds(self):
        print "*********************************"
        print "TEST: test_get_standard_feeds"
        print "*********************************"
        self.print_video_feed(self.youtube_service.GetTopRatedVideoFeed())
        self.print_video_feed(self.youtube_service.GetMostViewedVideoFeed())
        self.print_video_feed(self.youtube_service.GetRecentlyFeaturedVideoFeed())
        self.print_video_feed(self.youtube_service.GetWatchOnMobileVideoFeed())
        self.print_video_feed(self.youtube_service.GetTopFavoritesVideoFeed())
        self.print_video_feed(self.youtube_service.GetMostRecentVideoFeed())
        self.print_video_feed(self.youtube_service.GetMostDiscussedVideoFeed())
        self.print_video_feed(self.youtube_service.GetMostLinkedVideoFeed())
        self.print_video_feed(self.youtube_service.GetMostRespondedVideoFeed())
        # You can also retrieve a YouTubeVideoFeed by passing in the URI
        uri = 'http://gdata.youtube.com/feeds/api/standardfeeds/JP/most_viewed'
        self.print_video_feed(self.youtube_service.GetYouTubeVideoFeed(uri))

    def test_get_user_uploads(self):
        print "*********************************"
        print "TEST: test_get_standard_feeds"
        print "*********************************"
        uri = 'http://gdata.youtube.com/feeds/api/users/default/uploads'
        self.print_video_feed(self.youtube_service.GetYouTubeVideoFeed(uri))
    
    def test_upload_and_delete(self):
        # prepare a media group object to hold our video's meta-data
        media_group = gdata.media.Group(
            title=gdata.media.Title(text="Marko KCClass test."),
            description=gdata.media.Description(description_type='plain',
                text="Marko's test movie for the KC Class project."),
            keywords=gdata.media.Keywords(text='Marko, KCClass'),
            category=[gdata.media.Category(
                text='Education',
                scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                label='Education')],
                player=None)
        # create the gdata.youtube.YouTubeVideoEntry to be uploaded
        video_entry = gdata.youtube.YouTubeVideoEntry(media=media_group)
        # set the path for the video file binary
        video_file_location = '../sample-data/test-video1.flv'
        new_entry = self.youtube_service.InsertVideoEntry(video_entry, video_file_location)
        # check if he uploading was successful.
        upload_status = self.youtube_service.CheckUploadStatus(new_entry)
        if upload_status is not None:
            video_upload_state = upload_status[0]
            detailed_message = upload_status[1]
            print "%s: %s" % (video_upload_state, detailed_message)
        # list the uploaded videos.
        uri = 'http://gdata.youtube.com/feeds/api/users/default/uploads'
        feed = self.youtube_service.GetYouTubeVideoFeed(uri)
        for entry in feed.entry:
            self.print_entry_details(entry)
        # delete the video.
        response = self.youtube_service.DeleteVideoEntry(new_entry)
        if response:
            print 'Video successfully deleted!'
        else:
            print 'Video deletion failed!'
        

if __name__ == '__main__':
    unittest.main()