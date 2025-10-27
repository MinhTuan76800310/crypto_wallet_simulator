Wallet:
    Properties:
        - string: private_key 
            256 bit - 32 bytes: f8f8a2f43c8376ccb0871305060d7b27b0554d2cc72bccf41b2705608452f315
        - string: public_key
        - Address: wallet_address
    Methods:
        - __init__: Construct
            Function: 
                - Create key pair
        - generate_key_pair(string private_key) -> void
            Funtion: 
            - Random generate private key
                + 
            - Create public_key from private_key
        - create_transaction() -> Transaction

Transaction:


Cryptographic Hashing: Algorithms like SHA-256 and RIPEMD-160 are fundamental.

Key Derivation: Hierarchical Deterministic (HD) wallet derivation (BIP32/BIP44) involves numerous elliptic curve operations.

Transaction Signing: ECDSA signature generation is a CPU-bound task.

Simulation Logic: Simulating proof-of-work or other consensus mechanisms can be extremely demanding.