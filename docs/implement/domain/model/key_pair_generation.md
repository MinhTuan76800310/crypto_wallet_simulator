Term: 
    - Elliptic Curve Cryptography - ECC
    ![alt text](image.png)

In the system that using ECC (e.g, Bitcoin and Ethereum), the public key is the point in the Elliptic Curve Cryptography 
-> The public key can include a pair of coordinates (X, Y)

Type of Public key:
    - Uncompressed Public Key: Start with prefix 0x04 and the string of X coordinator (32 bytes), Y coordinator (32 byte) --> 65 bytes - 130 hex characters. 
    - Compressed Public Key: Start with prefix 0x02 and the string of X coordinator (32 bytes) if the Y coordinator is even. Else, It start with 0x03 --> 33 byte - 66 hex characters


