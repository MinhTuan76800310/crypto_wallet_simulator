The wallet address is calculated by hashing from public key.
Example:
    - In Bitcoin, the address is created by RIPEMD160(SHA256(K)) (K = piblic key), then cryptographize by Base58Check. The address of Bitcoin usually start with '1' or '3'
    - In Ethereum, the address is 20 byte at the end of 160 bit of hashed value by Keccak-256 (SHA-3) from Public Key K, not include prefix 04
