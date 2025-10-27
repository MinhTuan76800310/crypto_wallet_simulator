use wallet_core::wallet::Wallet;

#[test]
fn create_wallet_and_address() {
    let w = Wallet::new("alice");
    let addr = w.address();
    assert!(!addr.is_empty());
}
