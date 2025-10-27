pub mod bitcoin;
pub mod ethereum;

pub trait Network {
    fn broadcast(&self, payload: &str);
}
