use domain_model::{Transaction, TxIn, TxOut, UTXO, Address};

pub struct TransactionService;

impl TransactionService {
    pub fn create_transaction(&self, from: &Address, to: &Address, amount: f64, utxos: &[UTXO]) -> Option<Transaction> {
        let mut inputs = Vec::new();
        let mut total = 0.0;
        for u in utxos.iter().filter(|u| u.owner.0 == from.0) {
            inputs.push(TxIn { prev_tx_id: u.tx_id.clone(), index: u.index });
            total += u.amount;
            if total >= amount { break; }
        }
        if total < amount { return None; }
        let outputs = vec![TxOut { amount, address: to.clone() }];
        let tx = Transaction { tx_id: format!("tx-{}-{}", from.0, to.0), inputs, outputs };
        Some(tx)
    }
}
