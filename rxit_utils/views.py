from pyramid.view import view_config
from pyramid.response import Response, FileResponse
from rxit_utils.utilities.discern_orderable_extractor \
    import DiscernOrderableExtractor
from rxit_utils.utilities.pwrpln_color import color_updt_script
from rxit_utils.utilities.unrtf import unrtf_dataframe
import pandas as pd


# from rxit_utils.utilities.rtf_to_txt import striprtf

@view_config(route_name='home', renderer="templates/home_index.pt")
def home_index(request):
    return {'project': 'pyramid_app'}


@view_config(route_name='util_home',
             renderer='templates/utilities/util_home.pt')
def util_home(request):
    return {}


@view_config(route_name='discern_orderable',
             request_method='GET',
             renderer='templates/utilities/util_discern_orderable.pt')
def discern_orderable_uploader(request):
    return {}


@view_config(route_name='upload_discern_spreadsheet',
             request_method='POST',
             renderer='templates/utilities/util_discern_orderable.pt')
def upload_spreadsheet(request):
    import shutil
    from tempfile import NamedTemporaryFile

    # TODO: Add a button that downloads the dataframe as a CSV
    input_file = request.POST['spreadsheet'].file
    tmp = NamedTemporaryFile(mode='w+b')
    tmp_output = NamedTemporaryFile(mode='w+b', delete=False)
    try:
        shutil.copyfileobj(input_file, tmp)
        extractor = DiscernOrderableExtractor(tmp.name)
        combined_df = extractor.create_combined_df()

        results_tbl_html = combined_df.to_html(
            classes=['table', 'table-bordered'],
            table_id='dataTable',
        )

        # Create a tmp file to sit there in case user wants to download
        combined_df.to_csv(tmp_output.name)

    finally:
        pass

    return {
        'results': results_tbl_html,
        'results_dl_path': tmp_output.name,
    }


@view_config(route_name='download',
             request_method='POST',
             renderer='templates/utilities/util_discern_orderable.pt')
def download(request):
    """
    In the uploader, create the tmp_output, pass it over into the template
    so if a user requests the download, this function can serve that path
    """
    download_path = request.POST['download_path']
    response = FileResponse(download_path)
    response.content_disposition = 'attachment; filename="output.csv"'
    return response


@view_config(route_name='pwrpln_color',
             request_method='GET',
             renderer='templates/utilities/util_pwrpln_color.pt')
def pwrpln_color(request):
    return {}


@view_config(route_name='pwrpln_color_submit_form',
             request_method='POST',
             renderer='templates/utilities/util_pwrpln_color.pt')
def pwrpln_color_submit(request):
    pathway_comp_ids = request.POST['pathway_comp_ids']
    color_value = request.POST['color_value']
    return {'results': color_updt_script(color_value, pathway_comp_ids)}


@view_config(route_name='rtf_to_plaintext',
             renderer='templates/utilities/util_rtf.pt')
def rtf_to_plaintext(request):
    return {}


@view_config(route_name='upload_rtf_spreadsheet',
             request_method='POST',
             renderer='templates/utilities/util_rtf.pt')
def upload_rtf_spreadsheet(request):
    import shutil
    import textract
    from tempfile import NamedTemporaryFile

    # TODO: Add a button that downloads the dataframe as a CSV
    input_file = request.POST['spreadsheet'].file
    tmp = NamedTemporaryFile(mode='w+b')
    tmp_output = NamedTemporaryFile(mode='w+b', delete=False)

    try:
        rtf_df = pd.read_excel(input_file)
        rtf_df = unrtf_dataframe(rtf_df)
        results_tbl_html = rtf_df.to_html(
            classes=['table', 'table-bordered'],
            table_id='dataTable',
        )
        # Create a tmp file to sit there in case user wants to download
        rtf_df.to_csv(tmp_output.name)

    finally:
        pass

    return {
        'results': results_tbl_html,
        'results_dl_path': tmp_output.name,
    }


@view_config(route_name='ccl_home',
             renderer='templates/ccl_repo/ccl_home.pt')
def ccl_home(request):
    return {}
