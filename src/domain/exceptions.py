class DomainException(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)
        self.message = message


class InvalidSignatureException(DomainException):
    pass


class InsufficientFundsException(DomainException):
    def __init__(self, address=None, required: float = 0.0, available: float = 0.0, message: str = ""):
        msg = message or f"Insufficient funds for {address}: required={required}, available={available}"
        super().__init__(msg)
        self.address = address
        self.required = required
        self.available = available


class DoubleSpendException(DomainException):
    def __init__(self, utxo=None, message: str = ""):
        msg = message or "Double spend detected"
        super().__init__(msg)
        self.utxo = utxo


class InvalidTransactionException(DomainException):
    def __init__(self, transaction=None, message: str = ""):
        msg = message or "Invalid transaction"
        super().__init__(msg)
        self.transaction = transaction
