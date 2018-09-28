def validate_col_numeric(column_of_ids=None):
    """
    Goes through a column of id's and extracts only valid numbers to a new list
    :type column_of_ids: str
    :param column_of_ids: column of pathway_comp_ids, separated by newlines
    :return: list
    """
    input_list = column_of_ids.splitlines()

    output_list = []

    for val in input_list:
        try:
            output_list.append(str(float(val)))
        except ValueError:
            pass

    return output_list


def color_updt_script(color=None, pathway_comp_ids=None):
    """
    Returns a CCL update script to update colors for a set of pathway_comp_ids
    :type color: str
    :param color: Hex value of color to insert into update statement
    :type pathway_comp_ids: str
    :param pathway_comp_ids: column of pathway_comp_ids, separated by newlines
    """

    valid_pathway_comp_ids = validate_col_numeric(pathway_comp_ids)

    pathway_comp_ids_padded = ''

    # TODO: create a validation of inputs in the list
    # something like try: str(float(x)) except: ValueError
    # to create a separate list of valid entries to pass on to the update script
    # probably as a separate function to call in this one
    # probably also want to make sure that it will clear out blank entries

    for idx, id in enumerate(valid_pathway_comp_ids, 1):
        try:
            float(id)
            if idx % 5 == 0 and idx != len(valid_pathway_comp_ids):
                pathway_comp_ids_padded += id + ', \n'
            elif idx == len(valid_pathway_comp_ids):
                pathway_comp_ids_padded += id
            else:
                pathway_comp_ids_padded += id + ', '
        except ValueError:
            pass

    output_script: str = '''
update into PATHWAY_COMP
set DISPLAY_FORMAT_XML =
;Paste xml string between the single quotation marks below ''
'<?xml version="1.0"?>  <NoteFormat><Color><BackColor>00{0}</BackColor></Color></NoteFormat>'
    ,updt_id = reqinfo->updt_id
    ,updt_dt_tm = cnvtdatetime(curdate,curtime3)
    ,updt_cnt = updt_cnt +1
    ,updt_task = reqinfo->updt_task
    ,updt_applctx = reqinfo->updt_applctx
where comp_type_cd = (
    select cv.code_value
    from code_value cv
    where cv.code_set = 16750
    and cv.cdf_meaning = "NOTE")
and pathway_comp_id in (
{1}
)
go
commit go
        '''.format(color, pathway_comp_ids_padded)

    html_esc_output_script = output_script.replace('<', '&lt;')
    html_esc_output_script = html_esc_output_script.replace('>', '&gt;')

    return html_esc_output_script
