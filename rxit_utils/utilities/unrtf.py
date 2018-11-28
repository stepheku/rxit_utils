import pandas as pd
import subprocess


def find_rtf_col(df: pd.DataFrame) -> list:
    """Returns a list of dataframe columns whose values contain the string rtf1,
     implying that the values are in an RTF format"""
    col_list = []
    for col in df.columns:
        try:
            if df[col].str.contains('rtf1').any():
                col_list.append(col)
        except AttributeError:
            pass
    if col_list:
        return col_list
    else:
        return None


def unrtf(input_text: str = None):
    """Returns an RTF string with the RTF items removed, leaving the
    raw string intact"""

    splitter = b'-' * 17 + b'\n'

    if isinstance(input_text, str) and input_text != '':
        try:
            unrtf_text = subprocess.run(['unrtf', '--text'],
                                        stdout=subprocess.PIPE,
                                        input=input_text.encode('utf-8'))
            return unrtf_text.stdout.split(splitter)[-1].decode('utf-8',
                                                                'ignore')
        except AttributeError:
            return input_text
        except UnicodeDecodeError:
            print(
                'UnicodeDecodeError on line with value: {}'.format(input_text))
    else:
        return None


def unrtf_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Given a dataframe that has columns whose values are in an RTF format,
    returns a dataframe whose raw text has replaced the RTF format"""
    if find_rtf_col(df):
        for col in find_rtf_col(df):
            df[col + '2'] = df[col].apply(unrtf)
        return df
    else:
        return None
