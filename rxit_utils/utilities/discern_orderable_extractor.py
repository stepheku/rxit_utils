# TODO: Refactor the hell out of this

import collections
import re
import pandas as pd
from xlrd.biffh import XLRDError
from pandas.errors import ParserError

prim_regex = r'primary mnemonic is (?:.*?MUL.ORD!d\d{5}|\d{6,}\.0) (.*?) \d{3,}'
syn_regex = r'ordered as \d.*?\d{4,}\.0 (.*?) (?:2516|\d{4,})'
output_headers = ['Module name', 'Rule section',
                  'Synonym or Primary', 'Value']
expected_col = ['MODULE_NAME', 'MAINT_VALIDATION',
                'VERSION', 'DATA_TYPE', 'SECTION',
                'EKM_INFO']


def read_spreadsheet(spreadsheet_name):
    try:
        file_ext = spreadsheet_name.rsplit('.', 1)[1].lower()
        if file_ext == 'csv':
            return pd.read_csv(spreadsheet_name)
        elif file_ext == 'xlsx':
            return pd.read_excel(spreadsheet_name)
    except IndexError:
        pass
    else:
        return None


def validate_spreadsheet(spreadsheet_name):
    try:
        df = read_spreadsheet(spreadsheet_name)
        if set(expected_col) == set(df.columns):
            return True
        else:
            return False
    except (XLRDError, ParserError):
        return False


class DiscernOrderableExtractor:
    def __init__(self, input_file=None):
        if not isinstance(input_file, str):
            raise TypeError(
                '''The DiscernOrderableExtractor attribute {0} needs to be a 
                string of the file/path'''.format(input_file)
            )
        self.discern_rule_sections = ['Evoke Section', 'Logic Section',
                                      'Action Section']
        # self.data_frame = read_spreadsheet(input_file)

        self.data_frame = pd.read_excel(input_file)

    # TODO: Raise exception over here

    def create_orderable_df(self, orderable_type=None, regex_str=None):
        if orderable_type and regex_str:
            section_df = self.data_frame[
                self.data_frame['SECTION'].isin(self.discern_rule_sections)
            ]

            section_df['ORDERABLE'] = \
                section_df['EKM_INFO'].str.findall(regex_str)

            expl_orderable_df = section_df['ORDERABLE'] \
                .apply(pd.Series) \
                .stack() \
                .reset_index(level=1, drop=True) \
                .to_frame() \
                .reset_index()

            output_df = pd.merge(
                left=section_df.reset_index(),
                right=expl_orderable_df,
                left_on='index',
                right_on='index',
                how='inner'
            )

            output_df.drop(labels=['index', 'ORDERABLE', 'EKM_INFO'],
                           axis='columns', inplace=True)

            output_df.rename(columns={0: 'Orderable'}, inplace=True)

            output_df['ORDERABLE_TYPE'] = orderable_type

            return output_df

    def create_primaries_df(self):
        return self.create_orderable_df('Primary', prim_regex)

    def create_synonyms_df(self):
        return self.create_orderable_df('Synonym', syn_regex)

    def create_combined_df(self):
        df = self.create_primaries_df()
        return df.append(self.create_synonyms_df())

    def create_combined_df_csv(self, output_file):
        self.create_combined_df().to_csv(output_file)
