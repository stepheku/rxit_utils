from pyramid.view import view_config

@view_config(route_name='home', renderer="rxit_utils:templates/home_index.pt")
def home_index(request):
    return {'project': 'pyramid_app'}