Digital signature workflows:
    1. Hashing the transactions by SHA256 to create a message (receiver address, mount, fee, ...).
        -> Hashed transaction.
    2. The sender uses private key combine with a nounce to calculate *digital signature* in clliptic curve (ECDSA).
        -> Digital signature
    3. The receiver can use sender's public key and digital signature to verify the truelly of transaction.