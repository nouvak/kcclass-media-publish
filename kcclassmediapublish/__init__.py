from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = UnencryptedCookieSessionFactoryConfig('KCClassM3dIaPublishS3cr3t')
    config = Configurator(settings=settings, session_factory=my_session_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login/{provider}')
    config.add_route('login_response', '/login_response')
    config.add_route('list_media', '/media-list/{provider}')
    config.add_route('upload_media_show', '/media-upload/{provider}')
    config.add_route('upload_media_confirm', '/upload-media-confirm')
    config.add_route('delete_media', '/media-delete/{provider}/{id}')
    config.scan()
    return config.make_wsgi_app()
