from bitcoin.transaction import deserialize,txhash
from bitcoin.core.script import CScript
from bitcoin.wallet import CBitcoinAddress
import polars as pl

class BitcoinUtils:
    def __init__(self,encoded_btc_tx):
        self.encoded_btc_tx=encoded_btc_tx
        self.decoded_tx_obj=self.decode_transaction()
        self.decoded_dataframe=self.get_frame()
        
    def decode_script(self,script_hex):
        script = CScript(bytes.fromhex(script_hex))
        try:
            # Attempt to convert to a Bitcoin address
            address = CBitcoinAddress.from_scriptPubKey(script)
            return str(address)
        except ValueError:
            return 'Unknown or unsupported script type'

    def decode_transaction(self):
        tx = deserialize(self.encoded_btc_tx)
        txid = txhash(self.encoded_btc_tx)
        inputs = [{'txid': i['outpoint']['hash'], 'vout': i['outpoint']['index'], 'sequence': i['sequence']} for i in tx['ins']]
        outputs = [{'addresses': self.decode_script(o['script']), 'value': o['value']} for o in tx['outs']]
        return {'txid': txid, 'inputs': inputs, 'outputs': outputs}

    def get_frame(self):
        df=pl.DataFrame(self.decoded_tx_obj['outputs'])\
        .group_by(pl.col.addresses).agg(value=pl.col.value.sum())
        return df

    def contains_sanctioned_addresses(self):
        sanctioned_df=pl.read_parquet("btc_sanctioned_addresses.parquet")
        joined=sanctioned_df.join(self.decoded_dataframe,on='addresses')
        return len(joined)!=0

    def total_value(self,denomination="satoshi"):
        total=self.decoded_dataframe.select(pl.col.value.sum()).item()
        if denomination=="bitcoin":
            total=total/10**8
        return total

    def value_to(self,target_address,denomination="satoshi"):
        df=self.decoded_dataframe.filter(pl.col.addresses==target_address)
        amount=df.select(pl.col.value.sum()).item()
        if denomination=="bitcoin":
            amount=amount/10**8
        return amount

# # ### Example usage
# tx_hex = '020000000256fa13a0a1eb08466400ed0f54ec2787632006a01519c31948e424f665581fe7010000006a473044022054874771f4390c553e8421e71e3b6c8f36db1754b751841889f0ed81ca2c85f902200330680fe1de40830ef088501fca875eb8abac9f9fa910242ea22e9bf2fc6bbe012102679a681d9b5bf5c672e0413997762664a17009038674b806bf27dd6b368d9b67feffffff82dffb260bdb95d4329bfc9434189bba3a54d4c5bac308d8e8f18934ce7459a6010000006b483045022100d81cdb7ce0cfe2505c9413e754ba030cf8f2cf77edb766606a24cbfced82bfa7022007b713234fd88c470ba2d7c5fdfffec37efc9756e8f398da9a682cb58706ed85012102679a681d9b5bf5c672e0413997762664a17009038674b806bf27dd6b368d9b67feffffff1c2c9302000000000017a91406e525a64b998df7ed3f11912433a5547e017771873031370400000000160014989e28c2d186862f43c13e3334fb690bb2a8fd76c0e1e4000000000017a91489c8a00904121817360cc5f2a2d3ddb2607e515b8716c0b1000000000017a9142d03ebcb05fa454d206336108c1652bf18e2bc4087675858000000000017a914966379d9928c2d487492c1cba0600395d21573278786f10600000000001600140860c7a3b78c80e36a2bdd852cefb889d574a0f8b4bc1400000000001976a914310c2e97410549c55f6df94325533ae5d4e7d3d888acf4fb00000000000017a91423cd3bad1b87f70c6c2b5147447648db008592bb87748522000000000017a9149660dcf5caf9833eaa7363647771512c0b74982787b4102100000000001600148f3fe1ed19175b4523e153958bc4533ad1131dabe56d0d00000000001600144cddb8d067bd8ccd7d05d500090397ab93c54344ddf0110000000000160014dbc352e00dab50861c560a59cd80d04d8616dd5ca5300200000000001976a9142b49af3265e111b33f5c4326ae90be69d8090d1f88ace4701000000000001600140fde2948544cf8054120fe8487c2a4e2c2d0523194c104000000000017a9143aa4de68ea36c01c5a65c55bf26d30855dd4e9bb87dfbaff02000000001976a9145255a50a3ee18bcdddf431886727413ad7b2badd88acc0a410000000000016001401b02ce2c9a7effe1e365489dde04e97e3afa5e416724600000000001976a914353acfd3352f888c3389029483de6f570a6c4e2488ac30b9804a000000001976a91456f68436985b333da26fdafa0c6abbcf6121b3db88ac0cd601000000000016001416aa882387eb64bd56167793855da2ebbe4c77053cba8701000000001976a9145989d57d3b253824e6a62ec2f7b3f9e3f371c37288aca0c5b2000000000016001466f45f29e9af142970ea25d12d7b17c795e92ce73f4db621000000001600145fb7eb6e89cd0e16212e19eb475bf8c1ba750b7698c74e000000000016001454ffd4538fbef90fb375df0262ca656048b0459a7df906000000000017a9141b83ae1f29bab5773f8572911ad9621f3a8c798487bd145a0000000000160014dbc4ef483896d6ba0e4ac026e02a6d7c897ecc86dba71d00000000001976a914c4895e82afc158cc01fd0dac67e591c5773c6fff88ac2cc70200000000001600146f10ddb1201828097dd55f7ddfe66abb430cda5648b40a00'
# btc=BitcoinUtils(tx_hex)
# print(btc.decoded_dataframe)
# print(btc.decoded_tx_obj)
# print(btc.contains_sanctioned_addresses())
# print(btc.total_value(denomination="bitcoin"))
# print(btc.value_to("32KUV7TfdhmY5gGdemGUm7mYr31S56BpHb",denomination="bitcoin"))
