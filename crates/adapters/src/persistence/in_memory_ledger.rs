use domain_model::{UTXO, Block};

pub struct InMemoryLedger {
    pub blocks: Vec<Block>,
    pub utxos: Vec<UTXO>,
}

impl InMemoryLedger {
    pub fn new() -> Self { Self { blocks: Vec::new(), utxos: Vec::new() } }
}
