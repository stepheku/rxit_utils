"""
plan_csv_to_dict.py
~~~~~~~~~~~~~~~~~~~

Converts the PowerPlan CSV into a hierarchical dictionary
"""

from pathlib import Path
import argparse
import typing
import csv
import json
import re
from .xl_utils import general_utils as general_utils

STRING_ENCODING = "ISO-8859-1"
INVALID_CHARS = [b"\xc3\xaf", b"\xc2\xbb", b"\xc2\xbf", b"\x96"]
TREATMENT_PERIOD_REGEX = r"([^\|]*?) ?\((\d+) ([A-Za-z]+)\)"


def remove_nulls(s: typing.IO) -> typing.IO:
    for line in s:
        yield line.replace("\0", "")


def remove_invalid_chars(input_str: str) -> str:
    for char in INVALID_CHARS:
        if char in input_str.encode("utf-8")[:10]:
            input_str = input_str.replace(char.decode("utf-8"), "")
    return input_str


def double_escape_control_chars(input_str: str) -> str:
    substitutions = {"\n": "\\n", "\r": "\\r", "\t": "\\t"}
    checker = [s for s in substitutions if s in input_str]
    if not checker:
        return input_str
    else:
        return general_utils.replace_str_by_dict(input_str, substitutions)


def string_int_to_bool(input_str: str) -> bool:
    string_bool_map = {"0": False, "1": True}
    return string_bool_map[input_str]


def empty_str_check(input_str: str) -> int:
    """
    If str is empty, return 0, else return the number
    """
    if input_str is None:
        return 0
    elif (input_str.strip()) == "":
        return 0
    else:
        return int(float(input_str))


def remove_invalid_chars_from_csv_first_line(file_path: Path) -> Path:
    file_path_directory = file_path.cwd()
    file_path_tmp = Path(file_path_directory, "{}_tmp".format(file_path))
    with open(file_path_tmp, "w") as f:
        f.write("")
    with open(file_path, "r") as in_file:
        with open(file_path_tmp, "a") as out_file:
            out_file.write(remove_invalid_chars(in_file.readline()))
            for line in in_file.readlines():
                out_file.write(line)
    return file_path_tmp


def route_for_review_int_to_str(route_int: int) -> str:
    lookup_dict = {
        0: "Do not route for review",
        1: "Route for 1 review",
        2: "Route for 2 reviews",
    }
    return lookup_dict.get(route_int)


def create_powerplan_dict(input_file: str) -> dict:
    powerplan_dict = {}
    # with open(input_file, newline="", encoding=STRING_ENCODING) as csv_file:
    with open(input_file, newline="") as csv_file:
        # reader = csv.DictReader(remove_nulls(csv_file))
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                pathway_catalog_id = float(row.get("PATHWAY_CATALOG_ID"))
            except ValueError:
                continue

            pathway_catalog_id = float(row.get("PATHWAY_CATALOG_ID"))
            description = row.get("DESCRIPTION")
            display_description = row.get("DISPLAY_DESCRIPTION")
            plan_type = row.get("PLAN_TYPE")
            cross_encounter_ind = bool(row.get("CROSS_ENCOUNTER_IND"))
            evidence_link = row.get("EVIDENCE_LINK")
            check_alerts_on_planning_ind = bool(row.get("CHECK_ALERTS_ON_PLANNING_IND"))
            check_alerts_on_plan_updt_ind = bool(
                row.get("CHECK_ALERTS_ON_PLAN_UPDT_IND")
            )
            allow_diagnosis_propagation_ind = bool(
                row.get("ALLOW_DIAGNOSIS_PROPAGATION_IND")
            )
            hide_flexed_components = bool(row.get("HIDE_FLEXED_COMPONENTS"))
            cycle_use_numbers_ind = bool(row.get("CYCLE_USE_NUMBERS_IND"))
            cycle_std_nbr = row.get("CYCLE_STD_NBR")
            beg_cycle_nbr = row.get("BEG_CYCLE_NBR")
            end_cycle_nbr = row.get("END_CYCLE_NBR")
            cycle_incrm_nbr = row.get("CYCLE_INCRM_NBR")
            disp_std_nbr_or_end_val = row.get("DISP_STD_NBR_OR_END_VAL")
            restr_ability_to_mod_std_nbr = row.get("RESTR_ABILITY_TO_MOD_STD_NBR")
            cycle_disp_val = row.get("CYCLE_DISP_VAL")
            default_view_mean = row.get("DEFAULT_VIEW_MEAN")
            prompt_for_ordering_physician_ind = bool(
                row.get("PROMPT_FOR_ORDERING_PHYSICIAN_IND")
            )
            copy_forward_ind = bool(row.get("COPY_FORWARD_IND"))
            display_method = row.get("DISPLAY_METHOD")
            classification = row.get("CLASSIFICATION")
            plan_ord_def_prompt_user_ind = bool(row.get("PLAN_ORD_DEF_PROMPT_USER_IND"))
            plan_ord_def_open_default = row.get("PLAN_ORD_DEF_OPEN_DEFAULT")
            plan_ord_def_default_visit = row.get("PLAN_ORD_DEF_DEFAULT_VISIT")
            do_not_allow_proposal_ind = bool(row.get("DO_NOT_ALLOW_PROPOSAL_IND"))
            do_not_allow_plan_favorite = row.get("DO_NOT_ALLOW_PLAN_FAVORITE")
            first_phase_pathway_catalog_id = float(
                row.get("FIRST_PHASE_PATHWAY_CATALOG_ID")
            )
            route_for_review = route_for_review_int_to_str(
                int(row.get("ROUTE_FOR_REVIEW"))
            )
            if pathway_catalog_id not in powerplan_dict:
                powerplan_dict[pathway_catalog_id] = {
                    "pathway_catalog_id": pathway_catalog_id,
                    "description": description,
                    "display_description": display_description,
                    "plan_type": plan_type,
                    "cross_encounter_ind": cross_encounter_ind,
                    "evidence_link": evidence_link,
                    "check_alerts_on_planning_ind": check_alerts_on_planning_ind,
                    "check_alerts_on_plan_updt_ind": check_alerts_on_plan_updt_ind,
                    "allow_diagnosis_propagation_ind": allow_diagnosis_propagation_ind,
                    "hide_flexed_components": hide_flexed_components,
                    "cycle_use_numbers_ind": cycle_use_numbers_ind,
                    "cycle_std_nbr": cycle_std_nbr,
                    "beg_cycle_nbr": beg_cycle_nbr,
                    "end_cycle_nbr": end_cycle_nbr,
                    "cycle_incrm_nbr": cycle_incrm_nbr,
                    "disp_std_nbr_or_end_val": disp_std_nbr_or_end_val,
                    "restr_ability_to_mod_std_nbr": restr_ability_to_mod_std_nbr,
                    "cycle_disp_val": cycle_disp_val,
                    "default_view_mean": default_view_mean,
                    "prompt_for_ordering_physician_ind": prompt_for_ordering_physician_ind,
                    "copy_forward_ind": copy_forward_ind,
                    "display_method": display_method,
                    "classification": classification,
                    "plan_ord_def_prompt_user_ind": plan_ord_def_prompt_user_ind,
                    "plan_ord_def_open_default": plan_ord_def_open_default,
                    "plan_ord_def_default_visit": plan_ord_def_default_visit,
                    "do_not_allow_proposal_ind": do_not_allow_proposal_ind,
                    "do_not_allow_plan_favorite": do_not_allow_plan_favorite,
                    "first_phase_pathway_catalog_id": first_phase_pathway_catalog_id,
                    "route_for_review": route_for_review,
                    "phases": {},
                }

            powerplan = powerplan_dict[pathway_catalog_id]

            phase_sequence = int(row.get("PHASE_SEQUENCE"))
            phase_pathway_catalog_id = float(row.get("PHASE_PATHWAY_CATALOG_ID"))
            description = row.get("PHASE_DESCRIPTION")
            primary_phase_ind = string_int_to_bool(row.get("PRIMARY_PHASE_IND"))
            optional_phase_ind = string_int_to_bool(row.get("OPTIONAL_PHASE_IND"))
            future_phase_ind = string_int_to_bool(row.get("FUTURE_PHASE_IND"))
            this_visit_outpt = row.get("THIS_VISIT_OUTPT")
            this_visit_inpt = row.get("THIS_VISIT_INPT")
            future_visit_outpt = row.get("FUTURE_VISIT_OUTPT")
            future_visit_inpt = row.get("FUTURE_VISIT_INPT")
            check_alerts_on_planning_ind = string_int_to_bool(
                row.get("PHASE_CHECK_ALERTS_ON_PLANNING_IND")
            )
            check_alerts_on_plan_updt_ind = string_int_to_bool(
                row.get("PHASE_CHECK_ALERTS_ON_PLAN_UPDT_IND")
            )
            route_for_review = route_for_review_int_to_str(
                int(row.get("PHASE_ROUTE_FOR_REVIEW"))
            )    
            duration_qty = int(row.get("DURATION_QTY"))
            duration_unit = row.get("DURATION_UNIT")
            phase_offset_qty = int(row.get("PHASE_OFFSET_QTY"))
            phase_offset_unit = row.get("PHASE_OFFSET_UNIT")
            anchor_phase = row.get("ANCHOR_PHASE")
            treatment_sched = re.findall(
                TREATMENT_PERIOD_REGEX, row.get("TREATMENT_SCHED")
            )
            phase_class = row.get("PHASE_CLASS")

            if phase_pathway_catalog_id not in powerplan["phases"]:
                powerplan["phases"][phase_pathway_catalog_id] = {
                    "phase_sequence": phase_sequence,
                    "phase_pathway_catalog_id": phase_pathway_catalog_id,
                    "description": description,
                    "primary_phase_ind": primary_phase_ind,
                    "optional_phase_ind": optional_phase_ind,
                    "future_phase_ind": future_phase_ind,
                    "this_visit_outpt": this_visit_outpt,
                    "this_visit_inpt": this_visit_inpt,
                    "future_visit_outpt": future_visit_outpt,
                    "future_visit_inpt": future_visit_inpt,
                    "check_alerts_on_planning_ind": check_alerts_on_planning_ind,
                    "check_alerts_on_plan_updt_ind": check_alerts_on_plan_updt_ind,
                    "route_for_review": route_for_review,
                    "duration_qty": duration_qty,
                    "duration_unit": duration_unit,
                    "phase_offset_qty": phase_offset_qty,
                    "phase_offset_unit": phase_offset_unit,
                    "anchor_phase": anchor_phase,
                    "treatment_sched": treatment_sched,
                    "classification": phase_class,
                    "components": {},
                }

            phase = powerplan["phases"][phase_pathway_catalog_id]

            pathway_comp_id = float(row.get("PATHWAY_COMP_ID"))
            comp_sequence = int(row.get("COMP_SEQUENCE"))
            component_type = row.get("COMPONENT_TYPE")

            component = (
                json.loads(row.get("COMPONENT")).get("DJSON").get("ST")
            )

            no_default_order_sentence = string_int_to_bool(
                row.get("NO_DEFAULT_ORDER_SENTENCE")
            )
            required = string_int_to_bool(row.get("REQUIRED"))
            prechecked = string_int_to_bool(row.get("PRECHECKED"))
            time_zero_ind = string_int_to_bool(row.get("TIME_ZERO_IND"))
            time_zero_offset = row.get("TIME_ZERO_OFFSET")
            offset = row.get("OFFSET")
            bgcolor_red = int(row.get("BGCOLOR_RED"))
            bgcolor_blue = int(row.get("BGCOLOR_BLUE"))
            bgcolor_green = int(row.get("BGCOLOR_GREEN"))
            target_duration = row.get("TARGET_DURATION")
            dcp_clin_cat = row.get("DCP_CLIN_CAT")
            dcp_clin_sub_cat = row.get("DCP_CLIN_SUB_CAT")
            allow_proactive_eval = string_int_to_bool(row.get("ALLOW_PROACTIVE_EVAL"))
            chemo_ind = string_int_to_bool(row.get("CHEMO_IND"))
            chemo_related_ind = string_int_to_bool(row.get("CHEMO_RELATED_IND"))
            persistent_note = string_int_to_bool(row.get("PERSISTENT_NOTE"))
            linking_anchor_comp_ind = string_int_to_bool(
                row.get("LINKING_ANCHOR_COMP_IND")
            )
            linking_group_desc = row.get("LINKING_GROUP_DESC")
            linking_rule = row.get("LINKING_RULE")
            linking_rule_quantity = row.get("LINKING_RULE_QUANTITY")
            linking_override_reason = row.get("LINKING_OVERRIDE_REASON")
            comp_treatment_sched = re.findall(
                TREATMENT_PERIOD_REGEX, row.get("COMP_TREATMENT_SCHED")
            )
            scheduled_phase = row.get("SCHEDULED_PHASE")

            if pathway_comp_id not in phase["components"]:
                phase["components"][pathway_comp_id] = {
                    "pathway_comp_id": pathway_comp_id,
                    "comp_sequence": comp_sequence,
                    "component_type": component_type,
                    "component": component,
                    "no_default_order_sentence": no_default_order_sentence,
                    "required": required,
                    "prechecked": prechecked,
                    "time_zero_ind": time_zero_ind,
                    "time_zero_offset": time_zero_offset,
                    "offset": offset,
                    "bgcolor_red": bgcolor_red,
                    "bgcolor_blue": bgcolor_blue,
                    "bgcolor_green": bgcolor_green,
                    "target_duration": target_duration,
                    "dcp_clin_cat": dcp_clin_cat,
                    "dcp_clin_sub_cat": dcp_clin_sub_cat,
                    "allow_proactive_eval": allow_proactive_eval,
                    "chemo_ind": chemo_ind,
                    "chemo_related_ind": chemo_related_ind,
                    "persistent_note": persistent_note,
                    "linking_anchor_comp_ind": linking_anchor_comp_ind,
                    "linking_group_desc": linking_group_desc,
                    "linking_rule": linking_rule,
                    "linking_rule_quantity": int(linking_rule_quantity),
                    "linking_override_reason": linking_override_reason,
                    "treatment_sched": comp_treatment_sched,
                    "scheduled_phase": scheduled_phase,
                    "order_sentences": {},
                }

            component = phase["components"][pathway_comp_id]

            order_sentence_sequence = int(
                empty_str_check(row.get("ORDER_SENTENCE_SEQUENCE"))
            )
            order_sentence_id = float(empty_str_check(row.get("ORDER_SENTENCE_ID", 0)))
            order_sentence_display_line = row.get("ORDER_SENTENCE_DISPLAY_LINE")
            iv_ingredient = row.get("IV_INGREDIENT")
            iv_comp_syn_id = float(empty_str_check(row.get("IV_COMP_SYN_ID")))

            if row.get("ORDER_COMMENT"):
                order_comment = (
                    json.loads(row.get("ORDER_COMMENT")).get("DJSON").get("ST")
                )
            else:
                order_comment = ""

            if row.get("ORDER_SENTENCE_DETAIL"):
                pre_order_sentence_detail = (
                    json.loads(row.get("ORDER_SENTENCE_DETAIL")).get("DJSON").get("ST")
                )
                
                pre_order_sentence_detail = double_escape_control_chars(pre_order_sentence_detail)

                order_sentence_detail = json.loads(
                    pre_order_sentence_detail
                )
            else:
                order_sentence_detail = ""

            if order_sentence_id not in component["order_sentences"]:
                component["order_sentences"][order_sentence_id] = {
                    "order_sentence_sequence": order_sentence_sequence,
                    "order_sentence_id": order_sentence_id,
                    "order_sentence_display_line": order_sentence_display_line,
                    "iv_ingredient": iv_ingredient,
                    "iv_comp_syn_id": iv_comp_syn_id,
                    "order_comment": order_comment,
                    "order_sentence_detail": order_sentence_detail,
                }
    return powerplan_dict


def csv_to_dict(input_file: str = None):
    # input_file = remove_invalid_chars_from_csv_first_line(input_file)
    powerplan_dict = create_powerplan_dict(input_file)
    return powerplan_dict


if __name__ == "__main__":
    input_file = general_utils.get_args()
    powerplan_dict = create_powerplan_dict(input_file)