import logging

from kcclassmediapublish.services.youtube import YoutubeService
from kcclassmediapublish.services.picasaweb import PicassawebService
from kcclassmediapublish.services.slideshare import SlideshareService
from kcclassmediapublish.services.flickr import FlickrService
from kcclassmediapublish.metadata.publish_metadata import PublishMetadata,\
    Access

log = logging.getLogger( __name__ )

def create_service(service_name, username, password):
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
        log.error("Unknown service name: %s" % service_name)
        raise Exception("Unknown service name: " % service_name)
    return service

def create_publish_metadata(service_name):
    """
    Create an instance of a publishing metadata and fill it with the specifics 
    for the given multimedia provider.
    """
    metadata = PublishMetadata()
    if service_name == "youtube":
        metadata.category="Education"
        metadata.category=Access.PUBLIC
    elif service_name == "picassaweb":
        metadata.category="KCClass"
        metadata.category=Access.PUBLIC
    elif service_name == "slideshare":
        metadata.category="KCClass"
        metadata.category=Access.PUBLIC
    elif service_name == "flickr":
        metadata.category="KCClass"
        metadata.category=Access.PUBLIC
    else:
        log.error("Unknown service name: %s" % service_name)
        raise Exception("Unknown service name: " % service_name)
    return metadata