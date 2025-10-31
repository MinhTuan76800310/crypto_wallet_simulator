use thiserror::Error;

#[derive(Error, Debug)]
pub enum WalletError {
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Network request failed: {0}")]
    Network(#[from] reqwest::Error),

    #[error("Failed to parse derivation path: {0}")]
    DerivationPath(String),

    #[error("Insufficient funds: required {required}, but only have {available}")]
    InsufficientFunds {
        required: u64,
        available: u64,
    },
}