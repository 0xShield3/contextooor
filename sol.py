from solana.transaction import Transaction
import base64
import requests

class Snippets:

    def __init__(self,encoded_tx) -> None:
        self.decoded_tx=Transaction.deserialize(base64.b64decode(encoded_tx))
    
    def get_usd_value(self,lamports):
        value=requests.get(f"https://coins.llama.fi/prices/current/coingecko:solana").json()
        value=float(lamports)*float(value["coins"]["coingecko:solana"]['price'])/(10**9)
        return value

    def native_transfer_value(self,denomination="lamport"):
        bytes=self.decoded_tx.instructions[0].data
        
        int_list = [byte for byte in bytes]
        if int_list[:4]!=[2,0,0,0]:
            return "Error: this is not a native transfer."
        amount=int.from_bytes(int_list[4:],"little")
        if denomination=="solana":
            amount=amount/10**9
        if denomination=="usd":
            amount=self.get_usd_value(amount)
        return amount

    def get_addresses(self,denomination="lamport"):
        addrs=self.decoded_tx.compile_message().account_keys
        return [str(addr) for addr in addrs]
        

# print(Snippets("AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAED7JuzdbW/v+WSaCB647gzQXUnhGcBdxwdoOMdnTnatmkqlXfJ6t1HVw9V1KrCNL7Kfnwxlwp4fPQgVuUFwymbvQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAe6zoCIOKahUzMQNrDc0UYuk1to62CqqaBIcWay7GjFUBAgIAAQwCAAAAgJaYAAAAAAA=").native_transfer_value(denomination="usd"))

