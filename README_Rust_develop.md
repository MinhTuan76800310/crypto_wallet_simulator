# Understand Rust language
## Memory usage: **move** and **clone()**
**Stack Memory**: The stack is a highly organized region of memory that operates in a last-in, first-out (LIFO) manner. All data stored on the stack must have a known, fixed size at compile time. Pushing to and popping from the stack is extremely fast. Primitive types like *integers*, *booleans*, and *fixed-size arrays* are typically stack-allocated.  

**Heap Memory**: The heap is a less organized pool of memory used for data whose size is unknown at compile time or may change, such as a user-input String or a dynamically sized Vec<T>. When data is needed on the heap, the program requests a certain amount of space from the memory allocator. The allocator finds a suitable spot, marks it as in use, and returns a pointer (an address) to that location. This process is slower than stack allocation. Ownership's primary role is to manage this heap-allocated data, ensuring it is cleaned up precisely once when it's no longer needed.  

When a variable that owns heap data is assigned to another variable, Rust performs a move rather than a shallow copy. For example, with let s2 = s1; where s1 is a String, the pointer to the heap data is copied to s2, but s1 is immediately invalidated by the compiler. This prevents a "double free" error where both s1 and s2 would try to free the same memory when they go out of scope. If a deep copy of the heap data is required, it must be done explicitly with the .clone() method.   

## Borrowing and References

Accessing data without taking ownership. This is achieved through borrowing, which creates a reference to a value. A reference is like a pointer that is guaranteed to point to valid data. There are two types of borrows:

**Immutable Borrows (&T)**: An immutable reference allows read-only access to the data. The compiler enforces a critical rule: you can have any number of immutable references to a piece of data simultaneously.

**Mutable Borrows (&mut T)**: A mutable reference allows both reading and writing to the data. To prevent data races (where multiple pointers access the same data concurrently and at least one of the accesses is a write), the compiler enforces an even stricter rule: you can have only one mutable reference to a particular piece of data in a particular scope. Furthermore, you cannot have a mutable reference while any immutable references exist.   

*These rules are checked at compile time, providing what Rust calls "fearless concurrency" by eliminating entire classes of concurrency bugs before the program even runs.*

**The Hierarchy - structure of Project: Packages, Crates, and Modules**

Rust's code organization can be understood as a three-tiered hierarchy :  
- **Package**: The largest unit of code organization. A package is controlled by a Cargo.toml manifest file and can contain one or more crates. It defines dependencies, metadata, and build profiles.
- **Crate**: A compilation unit. A crate can be either a binary (an executable program with a main function) or a library (a collection of functionality intended to be used by other programs). Each crate has an implicit root module.
- **Module**: The primary way to organize code within a crate. Modules allow for grouping related functions, structs, and enums, and control their visibility.

**Paths for Access**: Items are accessed using paths.
- Absolute Paths start from the crate root, using the crate:: prefix (e.g., crate::networking::client::connect()).
- Relative Paths start from the current module, using keywords like self (the current module) or super (the parent module).   

The use Keyword: To avoid writing long, repetitive paths, the use keyword can bring items into the current scope, creating a convenient shortcut. It is idiomatic to bring the full path to structs and enums into scope, but only up to the parent module for functions to maintain clarity on where the function originates.  

File Organization: For larger projects, Rust allows modules to be split into separate files. If the crate root (src/main.rs or src/lib.rs) contains mod networking;, the compiler will look for the module's contents in either src/networking.rs or src/networking/mod.rs. This enables a clean, directory-based structure for complex codebases.   
*Example:*

MyProject/                  # 📦 PACKAGE
├── Cargo.toml             # Manifest file
└── src/
    ├── main.rs            # 🎯 BINARY CRATE (root)
    ├── lib.rs             # 📚 LIBRARY CRATE (root)  
    └── network/           # 📁 MODULE
        ├── mod.rs         # Module declaration
        └── client.rs      # Sub-module
--> Conclusion: Define sub-module in mod.rs -> sub-module.rs.

**Robust Error Handling**

Rust's approach to error handling is a significant departure from the exceptions used in Python and the mixed model of error codes and exceptions in C++. Rust treats potential failures as an explicit part of a program's control flow, forcing the developer to handle them at compile time. This is achieved through two powerful enums provided by the standard library: Option<T> and Result<T, E>.

- The Option<T> Enum: Handling Absence
```
pub enum Option<T> {
    None,    // Represents the absence of a value.
    Some(T), // Represents the presence of a value of type T.
}
```
- The Result<T, E> Enum: Handling Recoverable Errors

For operations that can fail in a recoverable way (e.g., network requests, file I/O), Rust uses the Result<T, E> enum. It is defined as:  
```
pub enum Result<T, E> {
    Ok(T),   // Represents a successful operation with a value of type T.
    Err(E),  // Represents a failure with an error value of type E.
}
```
```
fn process_transaction(amount: u64) -> Result<(), TransactionError> {
    if amount == 0 {
        return Err(TransactionError::InvalidAmount);
    }
    
    if amount > 1000 {
        return Err(TransactionError::InsufficientFunds);
    }
    
    // Xử lý transaction thành công
    println!("Processed transaction: {}", amount);
    Ok(())
}

#[derive(Debug)]
enum TransactionError {
    InvalidAmount,
    InsufficientFunds,
    NetworkError,
}
```
**Conclusion**: *By including the error type E in the function signature, Rust makes potential failures explicit and type-safe. The caller must handle the Err variant, preventing unhandled errors from crashing the program unexpectedly.*

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
        payload: Vec<u8>,l
    },
}
```


