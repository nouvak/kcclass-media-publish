import logging

from pyramid.view import view_config
from pyramid.response import Response
from kcclassmediapublish.upload.upload_file import get_file_from_user

log = logging.getLogger( __name__ )

#@view_config(route_name='home', renderer='templates/mytemplate.pt')
#def my_view(request):
#    return {'project':'kcclass-media-publish'}

@view_config(route_name='list-media', renderer='templates/media_list.pt')
def list_media(request):
    return {}

@view_config(route_name='upload-media-show', renderer='templates/media_upload.pt')
def upload_media_show(request):
    return {}

@view_config(route_name='upload-media-confirm')
def upload_file(request):
    # ``filename`` contains the name of the file in string format.
    #
    # WARNING: this example does not deal with the fact that IE sends an
    # absolute file *path* as the filename.  This example is naive; it
    # trusts user input.
    log.debug("Uploading file.")
    filename = request.POST['filepath'].filename
    log.debug("filename: " + filename);
    # 'filepath' contains the actual file data which needs to be
    # stored somewhere.
    input_file = request.POST['filepath'].file
    out_filepath = get_file_from_user(filename, input_file)
    log.debug("Output filepath: %s" % out_filepath)
    # get media metadata.
    
    # upload the media file to the selected media sites.
    media_site = request.POST['media-site']
    log.debug("Media site: %s" % media_site)
    if media_site == "youtube":
        pass
    elif media_site == "picasaweb":
        pass
    elif media_site == "slideshare":
        pass
    elif media_site == "flickr":
        pass
    else:
        log.error("Unidentified media site: " + media_site)        
    
    log.debug("Uploading succeeded.")
    return Response('OK')