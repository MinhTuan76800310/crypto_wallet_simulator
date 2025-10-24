from typing import Dict, Any, List, Optional, Callable
from domain.model import Address, Transaction, TxIn, TxOut, UTXO, Block, BlockHeader
from adapters.persistence import InMemoryLedgerRepository, LedgerRepository
from adapters.consensus import ProofOfWorkAdapter, MockProofOfStakeAdapter
from domain.exceptions import (
    InvalidSignatureException,
    InsufficientFundsException,
    DoubleSpendException,
    InvalidTransactionException,
)
import hashlib, time


class WalletService:
    def __init__(self):
        # simple in-memory wallet store: name -> (priv, pub, address)
        self._wallets: Dict[str, Dict[str, str]] = {}

    def create_wallet(self, name: str) -> Dict[str, str]:
        # deterministic stub keypair for now
        priv = hashlib.sha256((name + "_priv").encode()).hexdigest()
        pub = hashlib.sha256((priv + "_pub").encode()).hexdigest()
        address = Address.from_public_key(pub)
        self._wallets[name] = {"priv": priv, "pub": pub, "address": address}
        return self._wallets[name]

    def get_balance(self, address: Address, repo: LedgerRepository) -> float:
        utxos = [u for u in repo.all_utxos() if u.owner_address == address]
        return sum(u.amount for u in utxos)


class TransactionService:
    def __init__(self, repo: LedgerRepository):
        self.repo = repo

    def create_transaction(self, from_address: Address, outputs: List[TxOut]) -> Transaction:
        # collect UTXOs
        utxos = [u for u in self.repo.all_utxos() if u.owner_address == from_address]
        if not utxos:
            raise InsufficientFundsException(address=from_address, required=sum(o.amount for o in outputs), available=0)
        inputs: List[TxIn] = []
        total = 0.0
        for u in utxos:
            inputs.append(TxIn(prev_tx_id=u.tx_id, output_index=u.output_index))
            total += u.amount
            if total >= sum(o.amount for o in outputs):
                break
        if total < sum(o.amount for o in outputs):
            raise InsufficientFundsException(address=from_address, required=sum(o.amount for o in outputs), available=total)
        tx = Transaction(tx_id=None, inputs=inputs, outputs=outputs)
        tx.tx_id = tx.calculate_hash()
        return tx

    def sign_transaction(self, wallet_priv: str, tx: Transaction) -> None:
        tx_hash = tx.calculate_hash()
        for idx, _ in enumerate(tx.inputs):
            sig = hashlib.sha256((wallet_priv + tx_hash).encode()).digest()
            tx.add_signature(idx, sig)

    def verify_transaction(self, tx: Transaction, key_lookup: Callable[[TxIn], Optional[str]]) -> bool:
        try:
            return tx.verify(key_lookup)
        except Exception as e:
            raise InvalidTransactionException(transaction=tx, message=str(e))


class MiningService:
    def __init__(self, repo: LedgerRepository, pow_adapter: ProofOfWorkAdapter):
        self.repo = repo
        self.pow = pow_adapter

    def mine_block(self, transactions: List[Transaction], validator: str) -> Block:
        prev = self.repo.get_latest_block()
        prev_hash = prev.header.calculate_hash() if prev else "0" * 64
        header = BlockHeader(version=1, prev_hash=prev_hash, merkle_root="", timestamp=int(time.time()), nonce=0, difficulty=self.pow.difficulty, validator_id=validator)
        block = Block(header=header, transactions=transactions)
        block.header.merkle_root = block.calculate_merkle_root()
        block_hash = self.pow.mine(block.header)
        self.repo.add_block(block)
        # update utxo set: remove spent, add new outputs
        for tx in transactions:
            for inp in tx.inputs:
                self.repo.remove_utxo(f"{inp.prev_tx_id}:{inp.output_index}")
            for idx, out in enumerate(tx.outputs):
                utxo = UTXO(tx_id=tx.tx_id, output_index=idx, amount=out.amount, owner_address=out.address)
                self.repo.add_utxo(utxo)
        return block


class StakingService:
    def __init__(self, repo: LedgerRepository, pos_adapter: MockProofOfStakeAdapter):
        self.repo = repo
        self.pos = pos_adapter

    def stake_block(self, transactions: List[Transaction], validator: str) -> Block:
        # very simple PoS: no real stake calculation
        prev = self.repo.get_latest_block()
        prev_hash = prev.header.calculate_hash() if prev else "0" * 64
        header = BlockHeader(version=1, prev_hash=prev_hash, merkle_root="", timestamp=int(time.time()), nonce=0, difficulty=0, validator_id=validator)
        block = Block(header=header, transactions=transactions)
        block.header.merkle_root = block.calculate_merkle_root()
        # assume valid
        self.repo.add_block(block)
        for tx in transactions:
            for inp in tx.inputs:
                self.repo.remove_utxo(f"{inp.prev_tx_id}:{inp.output_index}")
            for idx, out in enumerate(tx.outputs):
                utxo = UTXO(tx_id=tx.tx_id, output_index=idx, amount=out.amount, owner_address=out.address)
                self.repo.add_utxo(utxo)
        return block

