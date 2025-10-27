wallet-simulator/
├── Cargo.toml         # Định nghĩa workspace
├── wallet-core/       # Crate thư viện cốt lõi (logic, không có hàm main)
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs     # Gốc crate, khai báo mô-đun, API công khai
│       ├── wallet.rs  # Struct Wallet, quản lý khóa, logic giao dịch
│       ├── crypto.rs  # Các nguyên thủy băm, ký, xác minh
│       ├── network/   # Logic và trait dành riêng cho blockchain
│       │   ├── mod.rs
│       │   ├── bitcoin.rs
│       │   └── ethereum.rs
│       ├── storage.rs # Logic lưu trữ (lưu/tải ví)
│       └── error.rs   # Các kiểu lỗi tùy chỉnh cho thư viện
├── wallet-cli/        # Crate nhị phân cho giao diện dòng lệnh
│   ├── Cargo.toml
│   └── src/
│       ├── main.rs    # Điểm vào ứng dụng, phân tích cú pháp CLI
│       └── commands.rs# Triển khai các lệnh con của CLI
└── tests/             # Các bài kiểm thử tích hợp cấp workspace
remain docs folder, convert my project to like above

#Note:#
Define modules in lib.rs

Quản lý Cấu hình với config và serde

- For handling inheritance, the Rust use "enum" combine with "match" expression, the example as below:
```
/@code

pub enum Transaction {
    Payment {
        to: Address,
        amount: u64,
    },
    Stake {
        validator: PublicKey,
        amount: u64,
    },
    ContractCall {
        contract_id: ContractId,
        payload: Vec<u8>,
    },
}
```