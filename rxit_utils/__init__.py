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

    config.add_route('rtf_to_plaintext',
                     '/utilities/rtf_to_plaintext')

    config.add_route('upload_rtf_spreadsheet',
                     '/utilities/upload_rtf_spreadsheet')

    config.add_route('onc_powerplan_dcw_generator',
                     '/utilities/onc_powerplan_dcw_generator')

    config.add_route('upload_onc_powerplan_dcw_spreadsheet',
                     '/utilities/upload_onc_powerplan_dcw_spreadsheet')

    config.scan()
    return config.make_wsgi_app()
