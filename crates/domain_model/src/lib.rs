//! Domain model crate: core entities for the simulator

#[derive(Debug, Clone)]
pub struct Address(pub String);

#[derive(Debug, Clone)]
pub struct UTXO {
    pub tx_id: String,
    pub index: u32,
    pub amount: f64,
    pub owner: Address,
}

#[derive(Debug, Clone)]
pub struct TxIn {
    pub prev_tx_id: String,
    pub index: u32,
}

#[derive(Debug, Clone)]
pub struct TxOut {
    pub amount: f64,
    pub address: Address,
}

#[derive(Debug, Clone)]
pub struct Transaction {
    pub tx_id: String,
    pub inputs: Vec<TxIn>,
    pub outputs: Vec<TxOut>,
}

#[derive(Debug, Clone)]
pub struct BlockHeader {
    pub prev_hash: String,
    pub merkle_root: String,
    pub nonce: u64,
}

#[derive(Debug, Clone)]
pub struct Block {
    pub header: BlockHeader,
    pub transactions: Vec<Transaction>,
}

#[derive(Debug)]
pub struct Chain {
    pub blocks: Vec<Block>,
}

impl Chain {
    pub fn new() -> Self {
        Self { blocks: Vec::new() }
    }

    pub fn tip(&self) -> Option<&Block> {
        self.blocks.last()
    }
}

#[derive(Debug, Clone)]
pub struct Wallet {
    pub name: String,
    pub address: Address,
}

impl Wallet {
    pub fn new(name: &str) -> Self {
        Self { name: name.to_string(), address: Address(name.to_string()) }
    }
}
