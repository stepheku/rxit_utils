from pyramid.view import view_config
from pyramid import httpexceptions
from pyramid.response import Response, FileResponse
from rxit_utils.utilities.discern_orderable_extractor \
    import DiscernOrderableExtractor
from rxit_utils.utilities.pwrpln_color import color_updt_script
from rxit_utils.utilities.unrtf import unrtf_dataframe
import pandas as pd
from rxit_utils import plan_dcw_generator
from pathlib import Path
from rxit_utils.view_models.shared.view_model_base import ViewModelBase

@view_config(route_name='util_home',
             renderer='rxit_utils:templates/utilities/util_home.pt')
def util_home(request):
    view_model = ViewModelBase(request)
    if not view_model.user_id:
        return httpexceptions.HTTPFound("/account/login")
    return view_model.to_dict()


@view_config(route_name='onc_powerplan_dcw_generator',
             renderer='rxit_utils:templates/utilities/util_dcw_generator.pt')
def util_dcw_generator(request):
    view_model = ViewModelBase(request)
    if not view_model.user_id:
        return httpexceptions.HTTPFound("/account/login")
    return view_model.to_dict()


@view_config(route_name='upload_onc_powerplan_dcw_spreadsheet',
             request_method='POST',
             renderer='rxit_utils:templates/utilities/util_dcw_generator.pt')
def upload_dcw_spreadsheet(request):
    import shutil
    import zipfile
    from tempfile import NamedTemporaryFile
    import tempfile

    tmp_path = Path(
        ".", "rxit_utils", "plan_dcw_generator", "data")

    # tmp_path = tempfile.TemporaryDirectory(dir=)
    
    # tmp_path = Path(tmp_path.name)

    input_file_name = request.POST['spreadsheet'].filename
    input_file = request.POST['spreadsheet'].file

    if Path(input_file_name).suffix.lower() == ".xlsx":
        tmp = NamedTemporaryFile(mode='w+b', delete=False, dir=tmp_path)
        df = pd.read_excel(input_file)
        df.to_csv(tmp.name)

    elif Path(input_file_name).suffix.lower() == ".csv":
        tmp = NamedTemporaryFile(mode='w+b', delete=False, dir=tmp_path)
        # tmp = Path(tmp_subpath, tmp_name).link_to(Path(tmp.name))
        shutil.copyfileobj(input_file, tmp)

    output_file_name = "powerplan_dcws.zip"
    output_file = Path(tmp_path, output_file_name)
    try:
        plan_dcw_generator.plan_dcw_generator.main(input_file=tmp.name)
        with zipfile.ZipFile(output_file, mode="w") as f:
            for dcw in tmp_path.glob("*.xlsx"):
                f.write(filename=dcw, arcname=dcw.name)
        
        for dcw in tmp_path.glob("*.xlsx"):
            dcw.unlink()

        response = FileResponse(str(output_file.resolve()), request=request, cache_max_age=86400)
        response.content_disposition = 'attachment; filename="{}"'.format(output_file_name)
    finally:
        pass

    return response

@view_config(route_name='discern_orderable',
             request_method='GET',
             renderer='rxit_utils:templates/utilities/util_discern_orderable.pt')
def discern_orderable_uploader(request):
    view_model = ViewModelBase(request)
    if not view_model.user_id:
        return httpexceptions.HTTPFound("/account/login")
    return view_model.to_dict()


@view_config(route_name='upload_discern_spreadsheet',
             request_method='POST',
             renderer='rxit_utils:templates/utilities/util_discern_orderable.pt')
def upload_spreadsheet(request):
    import shutil
    from tempfile import NamedTemporaryFile

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
             renderer='rxit_utils:templates/utilities/util_discern_orderable.pt')
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
             renderer='rxit_utils:templates/utilities/util_pwrpln_color.pt')
def pwrpln_color(request):
    view_model = ViewModelBase(request)
    if not view_model.user_id:
        return httpexceptions.HTTPFound("/account/login")
    return view_model.to_dict()


@view_config(route_name='pwrpln_color_submit_form',
             request_method='POST',
             renderer='rxit_utils:templates/utilities/util_pwrpln_color.pt')
def pwrpln_color_submit(request):
    pathway_comp_ids = request.POST['pathway_comp_ids']
    color_value = request.POST['color_value']
    return {'results': color_updt_script(color_value, pathway_comp_ids)}


@view_config(route_name='rtf_to_plaintext',
             renderer='rxit_utils:templates/utilities/util_rtf.pt')
def rtf_to_plaintext(request):
    view_model = ViewModelBase(request)
    if not view_model.user_id:
        return httpexceptions.HTTPFound("/account/login")
    return view_model.to_dict()


@view_config(route_name='upload_rtf_spreadsheet',
             request_method='POST',
             renderer='rxit_utils:templates/utilities/util_rtf.pt')
def upload_rtf_spreadsheet(request):
    from tempfile import NamedTemporaryFile

    # TODO: Add a button that downloads the dataframe as a CSV
    input_file = request.POST['spreadsheet'].file
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
