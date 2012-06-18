import logging
from pyslideshare import pyslideshare


from kcclassmediapublish.metadata.publish_metadata import PublishMetadata,\
    Access

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
                                                            slideshow_title=pub_metadata.title)
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
