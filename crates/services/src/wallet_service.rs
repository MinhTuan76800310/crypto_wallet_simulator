use domain_model::Wallet;

pub struct WalletService;

impl WalletService {
    pub fn create_wallet(&self, name: &str) -> Wallet {
        Wallet::new(name)
    }

    pub fn get_address(&self, wallet: &Wallet) -> String {
        wallet.address.0.clone()
    }
}
