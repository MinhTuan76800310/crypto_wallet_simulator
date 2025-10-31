use services::WalletService;

fn main() {
    let svc = WalletService;
    let w = svc.create_wallet("alice");
    println!("Wallet address: {}", w.address.0);
}
