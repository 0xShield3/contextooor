from bitcoin.core import CTransaction
from bitcoin.core.script import CScript
from bitcoin.wallet import CBitcoinAddress
import requests


class Snippets:
    def __init__(self, encoded_btc_tx):
        self.encoded_btc_tx = encoded_btc_tx
        self.decoded_tx_obj = self.decode_transaction()

    def decode_script(self, script_hex):
        script = CScript(script_hex)
        try:
            # Attempt to convert to a Bitcoin address
            address = CBitcoinAddress.from_scriptPubKey(script)
            return str(address)
        except ValueError:
            return 'Unable2Decode'

    def decode_transaction(self):
        tx = CTransaction.deserialize(bytes.fromhex(self.encoded_btc_tx))
        txid = tx.GetHash().hex()
        inputs = [{'txid': i.prevout.hash.hex(), 'vout': i.prevout.n,
                   'sequence': i.nSequence} for i in tx.vin]
        outputs = [{'addresses': self.decode_script(
            o.scriptPubKey), 'value': o.nValue} for o in tx.vout]
        return {'txid': txid, 'inputs': inputs, 'outputs': outputs}

    def get_usd_value(self, satoshis):
        value = requests.get(
            f"https://coins.llama.fi/prices/current/coingecko:bitcoin").json()
        value = float(satoshis) * \
            float(value["coins"]["coingecko:bitcoin"]['price'])/(10**8)
        return value

