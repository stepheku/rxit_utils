from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    config.add_static_view('static', 'static', cache_max_age=3600)

    # General page routes
    config.add_route('home', '/')

    # Utility routes
    config.add_route('util_home',
                     '/utilities')

    config.add_route('discern_orderable',
                     '/utilities/discern_orderable')

    config.add_route('upload_discern_spreadsheet',
                     '/utilities/upload_spreadsheet')

    config.add_route('download',
                     '/utilities/download')

    config.add_route('pwrpln_color',
                     '/utilities/powerplan_colors')

    config.add_route('pwrpln_color_submit_form',
                     '/utilities/powerplan_colors_submit')

    # CCL repo routes
    config.add_route('ccl_home',
                     '/ccl_repo')

    config.scan()
    return config.make_wsgi_app()
