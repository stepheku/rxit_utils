from typing import Optional

def try_int(text: str) -> Optional[int]:
    if text == "None":
        return None
    try:
        return int(text)
    except:
        return None