import argparse
import sys
from adapters.persistence import InMemoryLedgerRepository
from adapters.consensus import ProofOfWorkAdapter
from service_layer.services import WalletService, TransactionService, MiningService
from domain.model import Address, TxOut


def main():
    # ensure project root is importable
    parser = argparse.ArgumentParser(description="Simple Crypto Wallet Simulator CLI")
    sub = parser.add_subparsers(dest='cmd')

    p_init = sub.add_parser('init', help='Initialize simulator')

    p_create = sub.add_parser('create-wallet', help='Create a wallet')
    p_create.add_argument('name')

    p_tx = sub.add_parser('create-tx', help='Create a transaction')
    p_tx.add_argument('wallet_name')
    p_tx.add_argument('to_addr')
    p_tx.add_argument('amount', type=float)

    p_mine = sub.add_parser('mine', help='Mine a block')
    p_mine.add_argument('miner_name')

    args = parser.parse_args()

    # shared in-memory components
    repo = InMemoryLedgerRepository()
    wallet_service = WalletService()
    pow_adapter = ProofOfWorkAdapter(difficulty=2)
    tx_service = TransactionService(repo)
    miner = MiningService(repo, pow_adapter)

    if args.cmd == 'init':
        print('Simulator initialized (in-memory)')
    elif args.cmd == 'create-wallet':
        w = wallet_service.create_wallet(args.name)
        print('Created wallet:', w)
    elif args.cmd == 'create-tx':
        # find wallet
        w = wallet_service._wallets.get(args.wallet_name)
        if not w:
            print('Wallet not found')
            sys.exit(1)
        from_addr = w['address']
        to_addr = Address.from_public_key(args.to_addr) if len(args.to_addr) > 40 else Address(hash=args.to_addr)
        out = TxOut(amount=args.amount, address=to_addr)
        try:
            tx = tx_service.create_transaction(from_addr, [out])
            tx_service.sign_transaction(w['priv'], tx)
            print('Created and signed tx:', tx.tx_id)
        except Exception as e:
            print('Error creating tx:', e)
    elif args.cmd == 'mine':
        miner_wallet = wallet_service._wallets.get(args.miner_name)
        if not miner_wallet:
            print('Miner wallet not found')
            sys.exit(1)
        # mine empty block for now
        block = miner.mine_block([], validator=miner_wallet['address'].hash)
        print('Mined block with merkle root:', block.header.merkle_root)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
