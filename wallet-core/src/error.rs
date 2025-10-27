use thiserror::Error;

#[derive(Error, Debug)]
pub enum WalletError {
    #[error("Invalid Derivation Path: {0}")]
    InvalidDerivationPath(String),

    #[error("Crypto Error: {0}")]
    CryptoError(String),

    #[error("I/O Error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Serialization Error: {0}")]
    Serialization(#[from] serde_json::Error),

    #[error("Mnemonic Error: {0}")]
    Mnemonic(#[from] bip39::Error),

    #[error("Network Error: {0}")]
    Network(String),
}