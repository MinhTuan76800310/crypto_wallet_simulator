#[derive(Debug)]
pub struct DomainError(pub String);

#[derive(Debug)]
pub struct InvalidSignature(pub String);

#[derive(Debug)]
pub struct InsufficientFunds(pub String);

#[derive(Debug)]
pub struct DoubleSpend(pub String);

#[derive(Debug)]
pub struct InvalidTransaction(pub String);
