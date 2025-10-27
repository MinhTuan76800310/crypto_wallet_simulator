use super::Network;

pub struct BitcoinNetwork;

impl Network for BitcoinNetwork {
    fn broadcast(&self, payload: &str) {
        println!("[bitcoin] broadcast: {}", payload);
    }
}
