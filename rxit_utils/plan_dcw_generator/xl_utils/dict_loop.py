"""
dict_loop.py
~~~~~~~~~~~~~~~~~~~

Helper functions when doing dictionary loops (such as iterating based on a key)
"""


def get_comp_seq(item: tuple) -> int:
    """
    When iterating over dict.items(), this function can be used to sort by the
    nested dict key "comp_sequence"
    """
    return item[1].get("comp_sequence")


def get_phase_seq(item: tuple) -> int:
    """
    When iterating over dict.items(), this function can be used to sort by the
    nested dict key "
    """
    return item[1].get("phase_sequence")
    
def get_order_sentence_seq(item: tuple) -> int:
    """
    When iterating over dict.items(), this function can be used to sort by the
    nested dict key "order_sentence_sequence"
    """
    return item[1].get("order_sentence_sequence")