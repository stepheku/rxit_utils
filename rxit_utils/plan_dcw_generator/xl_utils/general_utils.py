"""
general_utils.py
~~~~~~~~~~~~~~~~~~~

All-purpose utilities for openpyxl
"""

import openpyxl
import re
import argparse
from pathlib import Path


def get_args() -> Path:
    """
    Parse arguments to returns a string for the file path that is
    given as an argument of the script
    """
    parser = argparse.ArgumentParser(
        description="Script that cleans up JSON text copied from the CCL prg"
    )

    parser.add_argument("--file_path", type=str, default=None, help="Path to the file")

    args = parser.parse_args()

    return Path(args.file_path)


def check_wb_obj(workbook):
    """
    Checks that function argument is an openpyxl.workbook object type
    """
    if not isinstance(workbook, openpyxl.Workbook):
        raise TypeError(
            "Argument given: {} is not a openpyxl.Workbook type".format(workbook)
        )


def check_toc_tab_exists(workbook: openpyxl.Workbook, sheet_name=None) -> bool:
    """
    Checks whether the workbook object provided contains the tab name
    provided
    """
    check_wb_obj(workbook)

    if not sheet_name:
        raise ValueError("Sheet name was not provided")

    if sheet_name not in [name for name in workbook.sheetnames]:
        raise ValueError(
            "Worksheet {} does not exist in workbook: {}".format(sheet_name, workbook)
        )

    return True


def bool_to_str(input_bool: bool) -> str:
    if input_bool:
        return "Yes"
    else:
        return "No"


def get_next_empty_row_in_col(
    col: int, worksheet: openpyxl.worksheet.worksheet.Worksheet, min_row: int = 1
):
    for row in worksheet.iter_cols(
        min_col=col, max_col=col, min_row=min_row, max_row=1000
    ):
        for cell in row:
            if (
                (cell.value is None)
                and (cell.offset(column=1).value is None)
                and (cell.offset(column=2).value is None)
                and (cell.offset(column=3).value is None)
                and (cell.offset(column=4).value is None)
            ):
                return cell.row
    # count = 0
    # for row in worksheet:
    #     if not all([cell.value == None for cell in row]):
    #         count += 1
    # return count


def replace_str_by_dict(input_str, substitutions: dict) -> str:
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile("|".join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], input_str)