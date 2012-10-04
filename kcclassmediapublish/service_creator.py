import logging

from kcclassmediapublish.services.youtube import YoutubeService
from kcclassmediapublish.services.picasaweb import PicassawebService
from kcclassmediapublish.services.slideshare import SlideshareService
from kcclassmediapublish.services.flickr import FlickrService

log = logging.getLogger( __name__ )

def create(service_name, username, password):
    """
    Create an instance of a multimedia publishing service given the service
    name.
    """
    log.debug("Creating service: %s" % service_name)
    if service_name == "youtube":
        service = YoutubeService(username, password)
    elif service_name == "picassaweb":
        service = PicassawebService(username, password)
    elif service_name == "slideshare":
        service = SlideshareService(username, password)
    elif service_name == "flickr":
        service = FlickrService(username, password)
    else:
        log.error("Undefined service name: %s" % service_name)
        service = None
    return service