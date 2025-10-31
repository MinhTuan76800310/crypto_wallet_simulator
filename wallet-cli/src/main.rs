use wallet_core::Wallet;

fn main() {
    let mut wallet = Wallet::new();
    
    match wallet.deposit(100) {
        Ok(()) => println!("Deposit successful!"),
        Err(e) => println!("Error: {}", e),
    }
    
    println!("Balance: {}", wallet.get_balance());
}