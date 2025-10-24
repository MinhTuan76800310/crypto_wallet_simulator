from dataclasses import dataclass, field
from typing import List, Optional, Dict, Callable
import hashlib
import time


@dataclass
class Address:
    hash: str

    @staticmethod
    def from_public_key(public_key: str) -> "Address":
        # simple address derivation: sha256 of public key
        h = hashlib.sha256(public_key.encode()).hexdigest()
        return Address(hash=h)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Address):
            return False
        return self.hash == other.hash

    def __hash__(self) -> int:
        return hash(self.hash)


@dataclass
class UTXO:
    tx_id: str
    output_index: int
    amount: float
    owner_address: Address
    lock_script: Optional[str] = None

    def is_spendable_by(self, address: Address) -> bool:
        return self.owner_address == address


@dataclass
class TxIn:
    prev_tx_id: str
    output_index: int
    signature_script: Optional[bytes] = None

    def reference_key(self) -> str:
        return f"{self.prev_tx_id}:{self.output_index}"


@dataclass
class TxOut:
    amount: float
    address: Address
    lock_script: Optional[str] = None


@dataclass
class Transaction:
    tx_id: Optional[str]
    inputs: List[TxIn]
    outputs: List[TxOut]
    signatures: Dict[int, bytes] = field(default_factory=dict)

    def calculate_hash(self) -> str:
        parts = []
        for inp in self.inputs:
            parts.append(f"{inp.prev_tx_id}:{inp.output_index}")
        for out in self.outputs:
            parts.append(f"{out.amount}:{out.address.hash}")
        raw = "|".join(parts)
        return hashlib.sha256(raw.encode()).hexdigest()

    def verify(self, key_lookup: Callable[[Address], Optional[str]]) -> bool:
        """Verify that each input has a signature and that the signature corresponds to the owner address.

        key_lookup(address) should return the owner's private key (or secret) used to create signatures.
        This is a simplified model for the simulator.
        """
        tx_hash = self.calculate_hash()
        for idx, inp in enumerate(self.inputs):
            if idx not in self.signatures:
                return False
            owner_priv = None
            # lookup owner by address via provided callback
            # key_lookup expects Address; we need owner address from UTXO context externally
            # For the simple verification model, the caller should supply a closure that returns
            # the private key for the address referenced by this input.
            owner_priv = key_lookup(inp)
            if owner_priv is None:
                return False
            expected = hashlib.sha256((owner_priv + tx_hash).encode()).digest()
            if expected != self.signatures[idx]:
                return False
        return True

    def add_signature(self, input_index: int, signature: bytes) -> None:
        self.signatures[input_index] = signature


@dataclass
class BlockHeader:
    version: int
    prev_hash: str
    merkle_root: str
    timestamp: int
    nonce: int = 0
    difficulty: int = 1
    validator_id: Optional[str] = None

    def calculate_hash(self) -> str:
        raw = f"{self.version}:{self.prev_hash}:{self.merkle_root}:{self.timestamp}:{self.nonce}:{self.difficulty}:{self.validator_id}"
        return hashlib.sha256(raw.encode()).hexdigest()


@dataclass
class Block:
    header: BlockHeader
    transactions: List[Transaction] = field(default_factory=list)

    def calculate_merkle_root(self) -> str:
        if not self.transactions:
            return hashlib.sha256(b'').hexdigest()
        tx_hashes = [t.calculate_hash() for t in self.transactions]
        while len(tx_hashes) > 1:
            if len(tx_hashes) % 2 == 1:
                tx_hashes.append(tx_hashes[-1])
            new_level = []
            for i in range(0, len(tx_hashes), 2):
                new_level.append(hashlib.sha256((tx_hashes[i] + tx_hashes[i+1]).encode()).hexdigest())
            tx_hashes = new_level
        return tx_hashes[0]

    def verify(self) -> bool:
        return self.header.merkle_root == self.calculate_merkle_root()

    def add_transaction(self, tx: Transaction) -> None:
        self.transactions.append(tx)
