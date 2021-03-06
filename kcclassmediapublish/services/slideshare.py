import logging
from pyslideshare import pyslideshare

from kcclassmediapublish.metadata.publish_metadata import PublishMetadata,\
    Access
from kcclassmediapublish.metadata.list_metadata import ListMetadata

log = logging.getLogger( __name__ )

class SlideshareService:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.api_key = '3U3jT35d'
        self.secret_key = 'OJLBwzkk'
        # authenticate the user.
        params = {
            'username': username,
            'password': password, 
            'api_key': self.api_key,
            'secret_key': self.secret_key
        }    
        self.slideshare_service = pyslideshare.pyslideshare(params, verbose=False)
            
    def publish(self, filepath, pub_metadata):
        """
        Publish the slide to the Slideshare cloud.
        """
        assert isinstance(filepath, basestring), "filepath is not string: " + str(filepath)
        assert isinstance(pub_metadata, PublishMetadata), "pub_metadata is not PublishMetadata" + str(pub_metadata)
        log.debug("Publishing Slideshare slide: %s, %s" % (filepath, str(pub_metadata)))
        response = self.slideshare_service.upload_slideshow(username=self.username, 
                                                            password=self.password, 
                                                            slideshow_srcfile=filepath,
                                                            slideshow_title=pub_metadata.title,
                                                            slideshow_tags=pub_metadata.tags)
        if response is None:
            raise Exception("Publishing failed.")
        slide_id = response.SlideShowUploaded.SlideShowID
        # publish image.
        log.debug("Publishing succeeded.")
        return slide_id

    
    def unpublish(self, slide_id):
        """
        Unpublish the image from the PicassaWeb cloud.
        """
        log.debug("Unpublishing Slideshare slide: %s" % str(slide_id))
        self.slideshare_service.delete_slideshow(username=self.username, 
                                                 password=self.password, 
                                                 slideshow_id=slide_id)
        log.debug("Unpublishing succeeded.")

    def list(self):
        """
        Return a list of published slideshows in SlideShare cloud for the given user.
        """
        log.debug("Listing the uploaded SlideShare photos.")
        feed = self.slideshare_service.get_slideshow_by_user( username_for=self.username )
        
        slideshows = []
        if feed is not None:
            if isinstance(feed['User']['Slideshow'], list):
                list_slideshow = feed['User']['Slideshow']
            else:
                list_slideshow = [feed['User']['Slideshow']]
            for entry in list_slideshow:
                video_id = str(entry['ID']['value'])
                title = entry['Title']['value']
                if 'value' in entry['Description']:
                    description = entry['Description']['value']
                else:
                    description = None
                category = None
                if 'value' in entry['Tags']:
                    tags = entry['Tags']['value']
                else:
                    tags = []
                slideshow_metadata = ListMetadata(id=video_id, title=title, 
                                                  description=description,
                                                  tags=tags, category=category)
                slideshows.append(slideshow_metadata)
        return slideshows

    def create_pub_metadata(self, request):
        pub_metadata = PublishMetadata()
        pub_metadata.title = request.POST['title']
        pub_metadata.description = request.POST['description']
        pub_metadata.tags = [t.strip() for t in request.POST['tags'].split(',')]
        pub_metadata.category = "KCClass"
        str_access = request.POST['access']
        if str_access == 'private':
            pub_metadata.access = Access.PRIVATE
        else:
            pub_metadata.access = Access.PUBLIC
        return pub_metadata
