
from dataclasses import dataclass
@dataclass
class cabrecord:
    freq:float
    mode: str
    when:str
    mycall:str
    myrst:str
    myexch:str
    dxcall:str
    dxrst:str
    dxexch:str
    txnum:int

