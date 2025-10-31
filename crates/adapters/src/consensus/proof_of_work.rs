pub struct ProofOfWork { pub difficulty: u32 }

impl ProofOfWork {
    pub fn new(difficulty: u32) -> Self { Self { difficulty } }
    pub fn mine(&self) -> String { "deadbeef".to_string() }
}
