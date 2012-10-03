import logging

from pyramid.view import view_config
from pyramid.response import Response
from kcclassmediapublish.upload.upload_file import get_file_from_user
from pyramid.decorator import reify
from pyramid.renderers import get_renderer

log = logging.getLogger( __name__ )

#@view_config(route_name='home', renderer='templates/mytemplate.pt')
#def my_view(request):
#    return {'project':'kcclass-media-publish'}

SERVICES_MENU = [
        {'href': 'youtube', 'title': 'YouTube'},
        {'href': 'picassaweb', 'title': 'Picasa web'},
        {'href': 'slideshare', 'title': 'SlideShare'},
        {'href': 'flickr', 'title': 'Flickr'},
]

def get_global_template():
    return get_renderer("templates/global_layout.pt").implementation()

def get_services_menu(request):
    new_menu = SERVICES_MENU[:]
    url = request.url
    for menu in new_menu:
        menu['current'] = url.endswith(menu['href'])
    return new_menu

def add_global_template_data(dct, request):
    dct['main'] = get_global_template()
    dct['services_menu'] = get_services_menu(request)
    return dct

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return add_global_template_data({}, request)

@view_config(route_name='login', renderer='templates/login.pt')
def login(request):
    provider = request.matchdict['provider']
    return add_global_template_data({'provider': provider}, request)
    
#@view_config(route_name='home', renderer='templates/media_list.pt')
@view_config(route_name='list-media', renderer='templates/media_list.pt')
def list_media(request):
    provider = request.matchdict.get('provider', 'youtube')
    log.debug("Listing media: provider=%s" % provider)
    return {}

@view_config(route_name='upload-media-show', renderer='templates/media_upload.pt')
def upload_media_show(request):
    log.debug("Displaying uploading form.")
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