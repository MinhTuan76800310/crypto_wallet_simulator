class ProofOfWorkAdapter:
    def __init__(self, difficulty: int = 2):
        self.difficulty = difficulty

    def mine(self, block_header):
        """Very simple PoW loop - returns hex digest when found."""
        import hashlib
        target = '0' * max(1, self.difficulty)
        nonce = 0
        while True:
            s = f"{block_header.prev_hash}{block_header.merkle_root}{nonce}{block_header.timestamp}".encode()
            h = hashlib.sha256(s).hexdigest()
            if h.startswith(target):
                block_header.nonce = nonce
                return h
            nonce += 1


class MockProofOfStakeAdapter:
    def __init__(self, validators=None):
        self.validators = validators or []

    def validate_block(self, block) -> bool:
        # placeholder: always valid
        return True

    def stake_block(self, transactions: list, validator: str):
        # build a header stub and return a Block-like dict for compatibility
        from domain.model import BlockHeader, Block
        import time
        prev_hash = "0" * 64
        header = BlockHeader(version=1, prev_hash=prev_hash, merkle_root="", timestamp=int(time.time()), nonce=0, difficulty=0, validator_id=validator)
        block = Block(header=header, transactions=transactions)
        block.header.merkle_root = block.calculate_merkle_root()
        return block
