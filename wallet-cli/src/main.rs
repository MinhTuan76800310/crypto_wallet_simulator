use anyhow::{Context, Result};

fn main() -> Result<()> {
    //... thiết lập...
    run_cli().context("Thao tác CLI thất bại")?;
    Ok(())
}

fn run_cli() -> Result<()> {
    //... phân tích cú pháp đối số và gọi vào wallet_core...
    let wallet = wallet_core::HDWallet::load("path/to/wallet.json")
      .context("Không thể tải ví từ đĩa")?;
    //...
    Ok(())
}
// Trong wallet-cli/src/main.rs
use serde::Deserialize;
use std::path::PathBuf;

#[derive(Debug, Deserialize)]
pub struct Settings {
    pub network: String,
    pub data_path: PathBuf,
    pub rpc_url: Option<String>,
}