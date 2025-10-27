use std::fs;
use std::path::Path;

pub fn save_wallet(path: &Path, data: &str) -> std::io::Result<()> {
    fs::write(path, data)
}

pub fn load_wallet(path: &Path) -> std::io::Result<String> {
    fs::read_to_string(path)
}
