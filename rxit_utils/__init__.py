from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    config.add_static_view('static', 'static', cache_max_age=3600)

    # General page routes
    config.add_route('home', '/')
    config.add_route('about', '/about')

    # Utility routes
    config.add_route('discern_orderable', '/utilities/discern_orderable')
    config.add_route('upload_discern_spreadsheet',
                     '/utilities/upload_spreadsheet')

    config.scan()
    return config.make_wsgi_app()