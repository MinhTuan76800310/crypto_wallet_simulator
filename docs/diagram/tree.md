## 🧩 Project Structure

```text
📦 crypto-wallet-simulator/
├── 📄 Cargo.toml                              # Workspace configuration
│
├── 📁 crates/
│   ├── 🧠 domain_model/                       # 🏗️ Core business logic
│   │   ├── 📄 Cargo.toml
│   │   └── 📁 src/
│   │       └── 🧩 lib.rs                      # Entities: Block, Transaction, Chain, Wallet
│   │
│   ├── ⚙️ services/                           # 🧰 Application layer (use cases)
│   │   ├── 📄 Cargo.toml
│   │   └── 📁 src/
│   │       ├── 🧩 lib.rs                      # Service traits
│   │       ├── 💼 wallet_service.rs           # Wallet operations
│   │       └── ⛏️ transaction_service.rs      # Transaction & mining operations
│   │
│   ├── 🔌 adapters/                           # 🔧 Infrastructure implementations
│   │   ├── 📄 Cargo.toml
│   │   └── 📁 src/
│   │       ├── 🧩 lib.rs
│   │       ├── 💾 persistence/                # Data storage adapters
│   │       │   ├── 📄 mod.rs
│   │       │   ├── 🗂️ in_memory_ledger.rs
│   │       │   └── 🧱 unit_of_work.rs
│   │       └── ⚖️ consensus/                 # Consensus algorithms
│   │           ├── 📄 mod.rs
│   │           ├── 🔨 proof_of_work.rs
│   │           └── 🌿 proof_of_stake.rs
│   │
│   ├── 🚨 error/                              # 🧩 Centralized error handling
│   │   ├── 📄 Cargo.toml
│   │   └── 📁 src/
│   │       └── 🧩 lib.rs
│   │
│   └── 🚀 crypto-wallet/                      # 🎯 Main application (composition root)
│       ├── 📄 Cargo.toml
│       └── 📁 src/
│           └── 🏁 main.rs
│
└── 🗃️ target/                                 # 🏭 Build artifacts
