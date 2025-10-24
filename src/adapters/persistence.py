from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from domain.model import Block, UTXO


class LedgerRepository(ABC):
    @abstractmethod
    def get_block(self, height: int) -> Optional[Block]:
        raise NotImplementedError()

    @abstractmethod
    def get_latest_block(self) -> Optional[Block]:
        raise NotImplementedError()

    @abstractmethod
    def add_block(self, block: Block) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_utxo(self, tx_id: str, index: int) -> Optional[UTXO]:
        raise NotImplementedError()

    @abstractmethod
    def add_utxo(self, utxo: UTXO) -> None:
        raise NotImplementedError()

    @abstractmethod
    def remove_utxo(self, utxo_key: str) -> None:
        raise NotImplementedError()


class InMemoryLedgerRepository(LedgerRepository):
    def __init__(self):
        self.blocks: List[Block] = []
        # utxo map keyed by "{tx_id}:{index}" -> UTXO
        self.utxo_set: Dict[str, UTXO] = {}

    def get_block(self, height: int) -> Optional[Block]:
        if 0 <= height < len(self.blocks):
            return self.blocks[height]
        return None

    def get_latest_block(self) -> Optional[Block]:
        if not self.blocks:
            return None
        return self.blocks[-1]

    def add_block(self, block: Block) -> None:
        self.blocks.append(block)

    def get_utxo(self, tx_id: str, index: int) -> Optional[UTXO]:
        return self.utxo_set.get(f"{tx_id}:{index}")

    def add_utxo(self, utxo: UTXO) -> None:
        key = f"{utxo.tx_id}:{utxo.output_index}"
        self.utxo_set[key] = utxo

    def remove_utxo(self, utxo_key: str) -> None:
        if utxo_key in self.utxo_set:
            del self.utxo_set[utxo_key]

    def all_utxos(self) -> List[UTXO]:
        return list(self.utxo_set.values())
