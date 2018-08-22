from pyramid.view import view_config
from pyramid.response import Response
from rxit_utils.utilities.discern_orderable_extractor \
    import DiscernOrderableExtractor


@view_config(route_name='home', renderer="templates/home_index.pt")
def home_index(request):
    return {'project': 'pyramid_app'}


@view_config(route_name='about', renderer="templates/home_about.pt")
def home_about(request):
    return { }


@view_config(route_name='discern_orderable',
             request_method='GET',
             renderer='templates/utilities/util_discern_orderable.pt')
def discern_orderable_uploader(request):
    return {}


@view_config(route_name='upload_discern_spreadsheet',
             request_method='POST',
             renderer='templates/utilities/util_discern_orderable.pt')
def upload_spreadsheet(request):
    import os
    import shutil
    from tempfile import NamedTemporaryFile

    # TODO: Add a button that downloads the dataframe as a CSV

    # ``filename`` contains the name of the file in string format.
    #
    # warning: internet explorer is known to send an absolute file
    # *path* as the filename.  This example is naive; it trusts
    # user input.
    filename = request.POST['spreadsheet'].filename

    # ``input_file`` contains the actual file data which needs to be
    # stored somewhere.
    input_file = request.POST['spreadsheet'].file

    # Using the filename like this without cleaning it is very
    # insecure so please keep that in mind when writing your own
    # file handling.
    file_path = os.path.join('/tmp', filename)

    # with open(file_path, 'wb') as output_file:
    #     shutil.copyfileobj(input_file, output_file)

    tmp = NamedTemporaryFile(mode='w+b')#, delete=False)
    try:
        shutil.copyfileobj(input_file, tmp)
        extractor = DiscernOrderableExtractor(tmp.name)
        # extractor.create_df_csv('output.csv')
        results_tbl_html = extractor.create_combined_df().to_html(
            classes=['table', 'table-bordered'],
            table_id='dataTable',
        )
    finally:
        pass
    # return Response('OK')
    return {'results': results_tbl_html}