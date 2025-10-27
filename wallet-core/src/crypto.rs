use sha2::{Sha256, Digest};

pub fn derive_private_key(seed: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(seed.as_bytes());
    hex::encode(hasher.finalize())
}

pub fn derive_public_key(priv_key: &str) -> String {
    // simplified: hash the private key
    let mut hasher = Sha256::new();
    hasher.update(priv_key.as_bytes());
    hex::encode(hasher.finalize())
}

pub fn address_from_pub(pub_key: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(pub_key.as_bytes());
    hex::encode(hasher.finalize())
}

pub fn sign(_priv_key: &str, data: &[u8]) -> Vec<u8> {
    // placeholder: return sha256(priv+data)
    let mut hasher = Sha256::new();
    hasher.update(_priv_key.as_bytes());
    hasher.update(data);
    hasher.finalize().to_vec()
}

pub fn verify(_pub_key: &str, data: &[u8], signature: &[u8]) -> bool {
    let expected = sign(_pub_key, data);
    expected == signature
}
