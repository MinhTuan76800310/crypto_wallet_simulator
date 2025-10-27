use crate::crypto;
use crate::error::WalletError;

/// A minimal Wallet struct that manages a keypair and simple tx creation.
pub struct Wallet {
    pub name: String,
    pub private_key: String,
    pub public_key: String,
}

impl Wallet {
    pub fn new(name: &str) -> Self {
        let private_key = crypto::derive_private_key(name);
        let public_key = crypto::derive_public_key(&private_key);
        Self {
            name: name.to_string(),
            private_key,
            public_key,
        }
    }

    pub fn address(&self) -> String {
        crypto::address_from_pub(&self.public_key)
    }

    pub fn sign(&self, data: &[u8]) -> Vec<u8> {
        crypto::sign(&self.private_key, data)
    }

    pub fn verify(&self, data: &[u8], signature: &[u8]) -> bool {
        crypto::verify(&self.public_key, data, signature)
    }

    pub fn create_transaction(&self, _to: &str, _amount: f64) -> Result<String, WalletError> {
        // Placeholder: build a serialized transaction string
        Ok(format!("tx:{}->{}:{}", self.address(), _to, _amount))
    }
}
