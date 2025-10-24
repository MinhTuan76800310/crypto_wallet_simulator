from dataclasses import dataclass
from typing import Any

@dataclass
class TxCreated:
    txid: str
    tx: Any

@dataclass
class TxSubmitted:
    txid: str

@dataclass
class BlockMined:
    block_hash: str
    block: Any
