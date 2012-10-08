import logging
from pyramid.view import view_config
from pyramid.response import Response
from kcclassmediapublish.upload.upload_file import get_file_from_user
from pyramid.renderers import get_renderer
from kcclassmediapublish import service_creator
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
from gdata.service import BadAuthentication

log = logging.getLogger( __name__ )

#@view_config(route_name='home', renderer='templates/mytemplate.pt')
#def my_view(request):
#    return {'project':'kcclass-media-publish'}

SERVICES_MENU = {
        'youtube': {'href': 'youtube', 'title': 'YouTube'},
        'picassaweb': {'href': 'picassaweb', 'title': 'Picasa web'},
        'slideshare': {'href': 'slideshare', 'title': 'SlideShare'},
        'flickr': {'href': 'flickr', 'title': 'Flickr'},
}

def get_global_template():
    return get_renderer('templates/global_layout.pt').implementation()

def get_services_menu(request):
    new_menu = SERVICES_MENU.copy()
    url = request.url
    for menu_key in new_menu:
        new_menu[menu_key]['current'] = url.endswith(new_menu[menu_key]['href'])
    return new_menu

def get_service(request, provider):
    session = request.session
    service_key = get_service_key(provider)
    return session.get(service_key, None)

def get_service_key(provider):
    return 'service_' + provider

def add_global_template_data(dct, request):
    dct['main'] = get_global_template()
    dct['services_menu'] = get_services_menu(request)
    return dct

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return add_global_template_data({}, request)

@view_config(route_name='login', renderer='templates/login.pt', request_method='GET')
def login(request):
    provider = request.matchdict['provider']
    return add_global_template_data({'provider': provider}, request)

@view_config(route_name='login_response', renderer='templates/login.pt', request_method='POST')
def login_response(request):
    provider = request.params['provider']
    username = request.params['inputUsername']
    password = request.params['inputPassword']
    try:
        service = service_creator.create(provider, username, password)
        if service is not None:
            session = request.session
            service_key = get_service_key(provider)
            session[service_key] = service
            return HTTPFound(route_url('list_media', request, provider=provider))
    except BadAuthentication, e:
        error = 'Incorrect username or password.'
    except Exception, e:
        error = 'Login failed.'
        log.error('Service creation failed: ' + str(e))
    return add_global_template_data({'error_msg': error, 'provider': provider}, request)
#    try:
#        appstruct = myform.validate(controls)
#    except ValidationFailure, e:
#        return {'form':e.render(), 'values': False}
#    # Process the valid form data, do some work
#    values = {
#        'name': appstruct['name'],
#        'shoe_size': appstruct['shoe_size'],
#        }
#    return {'form': myform.render(), 'values': values}
    
#@view_config(route_name='home', renderer='templates/media_list.pt')
@view_config(route_name='list_media', renderer='templates/media_list.pt')
def list_media(request):
    provider = request.matchdict.get('provider', 'youtube')
    service = get_service(request, provider)
    if service is None:
        return HTTPFound(route_url('login', request, provider=provider))
    log.debug('Listing media: provider=%s' % provider)
    media_list = service.list()
    return add_global_template_data({'provider': provider, 'media_list': media_list}, request)

@view_config(route_name='upload_media_show', renderer='templates/media_upload.pt')
def upload_media_show(request):
    log.debug('Displaying uploading form.')
    return add_global_template_data({}, request)

@view_config(route_name='upload_media_confirm')
def upload_file(request):
    # ``filename`` contains the name of the file in string format.
    #
    # WARNING: this example does not deal with the fact that IE sends an
    # absolute file *path* as the filename.  This example is naive; it
    # trusts user input.
    log.debug('Uploading file.')
    filename = request.POST['filepath'].filename
    log.debug('filename: ' + filename);
    # 'filepath' contains the actual file data which needs to be
    # stored somewhere.
    input_file = request.POST['filepath'].file
    out_filepath = get_file_from_user(filename, input_file)
    log.debug('Output filepath: %s' % out_filepath)
    # get media metadata.
    
    # upload the media file to the selected media sites.
    media_site = request.POST['media-site']
    log.debug('Media site: %s' % media_site)
    if media_site == 'youtube':
        pass
    elif media_site == 'picasaweb':
        pass
    elif media_site == 'slideshare':
        pass
    elif media_site == 'flickr':
        pass
    else:
        log.error('Unidentified media site: ' + media_site)
    log.debug('Uploading succeeded.')
    return Response('OK')

@view_config(route_name='delete_media')
def delete_media(request):
    provider = request.matchdict.get('provider', 'youtube')
    media_id = request.matchdict.get('id', None)
    service = get_service(request, provider)
    if service is None:
        return HTTPFound(route_url('login', request, provider=provider))
    log.debug('Deleting media: provider=%s, id=%s' % (provider, media_id))
    try:
        service.unpublish(media_id);
    except Exception, e:
        log.error('Unpublishing failed: ' + str(e))
    media_list = service.list()
    
    return add_global_template_data({'provider': provider, 'media_list': media_list}, request)
