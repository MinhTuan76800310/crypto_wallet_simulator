use super::Network;

pub struct EthereumNetwork;

impl Network for EthereumNetwork {
    fn broadcast(&self, payload: &str) {
        println!("[ethereum] broadcast: {}", payload);
    }
}
