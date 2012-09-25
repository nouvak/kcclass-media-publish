from pyramid.config import Configurator
from kcclassmediapublish.views import list_media

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('list-media', '/media-list/{provider}')
    config.add_route('upload-media-show', '/media-upload')
    config.add_route('upload-media-confirm', '/upload-media-confirm')
    config.scan()
    return config.make_wsgi_app()
