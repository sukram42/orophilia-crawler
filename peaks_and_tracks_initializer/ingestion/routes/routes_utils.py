from typing import Optional, Union


def convert_uiaa(uiaa: Optional[Union[str, int]])-> int:
    if uiaa is None: 
        return -1
    
    if isinstance(uiaa, int):
        return uiaa
    
    try: 
        return int(uiaa)
    except ValueError as e:
        pass

    uiaa ={
        "I": 1,
        "II": 2, 
        "III": 3,
        "IV": 4,
        "V": 5, 
        "VI": 6,
        "VII": 7, 
        "VIII": 8, 
    }.get(uiaa.upper())

    if uiaa is None:
         return -1
    return uiaa



