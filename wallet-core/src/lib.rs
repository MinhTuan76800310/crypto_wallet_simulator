pub struct Wallet {
    balance: u64,
}

impl Wallet {
    pub fn new() -> Self {
        Wallet { balance: 0 }
    }
    
    pub fn deposit(&mut self, amount: u64) -> Result<(), String> {
        if amount == 0 {
            return Err("Amount cannot be zero".to_string());
        }
        self.balance += amount;
        Ok(())
    }
    
    pub fn get_balance(&self) -> u64 {
        self.balance
    }
}