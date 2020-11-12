'''
borders.py
~~~~~~~~~~~~~~~~~~~~
This module contains openpyxl utilities specifically for setting
borders on given cells
'''

import openpyxl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.colors import Color


def set_outside_borders(cell: openpyxl.cell.cell.Cell) -> openpyxl.cell.cell.Cell:
    '''
    Sets all outside borders of a given cell
    '''
    if not isinstance(cell, openpyxl.cell.cell.Cell):
        # raise ValueError('Argument given is not a cell object type')
        pass

    side_properties = Side(
        style='medium', color=Color(rgb='00000000', auto=True, type='auto')
    )

    border_properties = Border(
        left=side_properties,
        right=side_properties,
        top=side_properties,
        bottom=side_properties
    )

    cell.border = border_properties

    return cell


def set_top_bot_borders(cell: openpyxl.cell.cell.Cell) -> openpyxl.cell.cell.Cell:
    '''
    Sets the top and bottom borders of a given cell
    '''
    if not isinstance(cell, openpyxl.cell.cell.Cell):
        raise ValueError('Argument given is not a cell object type')

    side_properties = Side(
        style='medium', color=Color(rgb='00000000', auto=True, type='auto')
    )

    border_properties = Border(
        top=side_properties,
        bottom=side_properties
    )

    cell.border = border_properties

    return cell


def set_top_bot_r_borders(cell: openpyxl.cell.cell.Cell) -> openpyxl.cell.cell.Cell:
    '''
    Sets the top, bottom and right borders of a given cell
    '''
    if not isinstance(cell, openpyxl.cell.cell.Cell):
        raise ValueError('Argument given is not a cell object type')

    side_properties = Side(
        style='medium', color=Color(rgb='00000000', auto=True, type='auto')
    )

    border_properties = Border(
        right=side_properties,
        top=side_properties,
        bottom=side_properties
    )

    cell.border = border_properties

    return cell


def set_top_bot_l_borders(cell: openpyxl.cell.cell.Cell) -> openpyxl.cell.cell.Cell:
    '''
    Sets the top, bottom and left borders of a given cell
    '''
    if not isinstance(cell, openpyxl.cell.cell.Cell):
        raise ValueError('Argument given is not a cell object type')

    side_properties = Side(
        style='medium', color=Color(rgb='00000000', auto=True, type='auto')
    )

    border_properties = Border(
        left=side_properties,
        top=side_properties,
        bottom=side_properties
    )

    cell.border = border_properties

    return cell
