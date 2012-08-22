import logging
import gdata.media
import gdata.youtube.service

from kcclassmediapublish.metadata.publish_metadata import PublishMetadata,\
    Access
from kcclassmediapublish.metadata.list_metadata import ListMetadata
from atom import Id

log = logging.getLogger( __name__ )

class YoutubeService:
    
    def __init__(self, username, password):
        self.youtube_service = gdata.youtube.service.YouTubeService()
        # Turn on HTTPS/SSL access.
        # Note: SSL is not available at this time for uploads.
        self.youtube_service.ssl = False
        # insert developer key for the publishing application.
        self.youtube_service.developer_key = 'AI39si6-qCVmA8KI53Eg3NF5VjnsvKYzsmzD4njj0VFnQDWgh-Iv0X3h_ABBCAwMWDe_G3VzEHGcTrd6eAy9QBPKBb3CDDDXJw'
        self.youtube_service.client_id = 'kcclass-media-publish'
        # authenticate the user.
        self.youtube_service.ClientLogin(username, password)
    
    def publish(self, filepath, pub_metadata):
        """
        Publish the video to the YouTube cloud.
        """
        assert isinstance(filepath, basestring), "filepath is not string: " + str(filepath)
        assert isinstance(pub_metadata, PublishMetadata), "pub_metadata is not PublishMetadata" + str(pub_metadata)
        log.debug("Publishing youtube video: %s, %s" % (filepath, str(pub_metadata)))
        # prepare a media group object to hold our video's meta-data
        if pub_metadata.access == Access.PRIVATE:
            is_private = gdata.media.Private()
        else:
            is_private = None
        media_group = gdata.media.Group(
            title=gdata.media.Title(text=pub_metadata.title),
            description=gdata.media.Description(description_type='plain',
                text=pub_metadata.description),
            keywords=gdata.media.Keywords(text=",".join(pub_metadata.tags)),
            category=[gdata.media.Category(
                text=pub_metadata.category,
                scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                label=pub_metadata.category)],
            player=None,
            private=is_private)
        # create the gdata.youtube.YouTubeVideoEntry to be uploaded
        video_entry = gdata.youtube.YouTubeVideoEntry(media=media_group)
        # set the path for the video file binary
        video_id = self.youtube_service.InsertVideoEntry(video_entry, filepath)
        # check if he uploading was successful.
        upload_status = self.youtube_service.CheckUploadStatus(video_id)
        if upload_status is not None:
            video_upload_state = upload_status[0]
            detailed_message = upload_status[1]
            log.debug("%s: %s" % (video_upload_state, detailed_message))
        log.debug("Publishing succeeded.")
        return video_id
    
    def unpublish(self, video_id):
        """
        Unpublish the video from the YouTube cloud.
        """
        log.debug("Unpublishing Youtube video: %s" % str(video_id))
        response = self.youtube_service.DeleteVideoEntry(video_id)
        if response is not None:
            log.debug("Unpublishing succeeded.")
        else:
            raise Exception("Unpublishing failed.")
        
    def list(self):
        """
        Return a list of published videos in YouTube cloud for the given user.
        """
        log.debug("Listing the uploaded youtube videos.")
        uri = 'http://gdata.youtube.com/feeds/api/users/default/uploads'
        feed = self.youtube_service.GetYouTubeVideoFeed(uri)
        videos = []
        for entry in feed.entry:
            video_id = entry.id.text
            title = entry.media.title.text
            description = entry.media.description.text
            if len(entry.media.category) > 0:
                category = entry.media.category[0].text
            else:
                category = None
            tags = entry.media.keywords.text.split(",")
            video_metadata = ListMetadata(id=video_id, title=title, 
                                          description=description,
                                          tags=tags, category=category)
            videos.append(video_metadata)
        return videos
