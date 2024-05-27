## Generate Base64 encoded transaction
from solana.transaction import Transaction

transaction = {
    "signer_id": "sender.testnet",
    "public_key": "ed25519:3tHbQxQkHmB2Qgnnsz4JikjiKEzA2x7fb7njt5eQ9MnN",
    "nonce": 1,
    "receiver_id": "receiver.testnet",
    "actions": [
        {"type": "Transfer", "amount": "1000000000000000000000000"}  # 1 NEAR in yoctoNEAR
    ],
    "block_hash": "11111111111111111111111111111111"
}
print(Transaction.serialize(transaction))

