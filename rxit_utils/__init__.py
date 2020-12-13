from pyramid.config import Configurator
from rxit_utils.data.db_session import DbSession
from pathlib import Path

def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    config = Configurator(settings=settings)
    init_includes(config)
    init_db(config)
    init_routing(config)
    return config.make_wsgi_app()


def init_includes(config):
    config.include("pyramid_chameleon")


def init_routing(config):
    config.add_static_view("static", "static", cache_max_age=3600)

    # General page routes
    config.add_route("home", "/")

    # Utility routes
    config.add_route("util_home", "/utilities")

    config.add_route("discern_orderable", "/utilities/discern_orderable")

    config.add_route("upload_discern_spreadsheet", "/utilities/upload_spreadsheet")

    config.add_route("download", "/utilities/download")

    config.add_route("pwrpln_color", "/utilities/powerplan_colors")

    config.add_route("pwrpln_color_submit_form", "/utilities/powerplan_colors_submit")

    config.add_route("rtf_to_plaintext", "/utilities/rtf_to_plaintext")

    config.add_route("upload_rtf_spreadsheet", "/utilities/upload_rtf_spreadsheet")

    config.add_route(
        "onc_powerplan_dcw_generator", "/utilities/onc_powerplan_dcw_generator"
    )

    config.add_route(
        "upload_onc_powerplan_dcw_spreadsheet",
        "/utilities/upload_onc_powerplan_dcw_spreadsheet",
    )


    config.add_route('account_home', '/account')
    config.add_route('login', '/account/login')
    config.add_route('register', '/account/register')
    config.add_route('logout', '/account/logout')

    config.scan()

def init_db(config):
    db_folder = Path(__file__).parent.absolute()
    db_file = str(Path(db_folder, "db", "rxit_utils.sqlite").absolute())
    DbSession.global_init(db_file=db_file)