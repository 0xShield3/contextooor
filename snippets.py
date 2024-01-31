from web3 import Web3
import requests

class Snippets:

    def __init__(self,w3=Web3(Web3.HTTPProvider("https://eth.public-rpc.com")),etherscan_api_key="PGJ5AYE9WGD77YPS4F3NGQ33MB5YI7JYS8"):
        self.etherscan_api_key=etherscan_api_key
        self.web3=w3
        try:
            self.web3.eth.get_block_number()
        except Exception:
            self.web3=Web3(Web3.HTTPProvider("https://eth.public-rpc.com"))
        self.v2_pair_abi="""[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]"""

    def get_usd_value(self,token):
        formatted_address="ethereum:"+token
        value=requests.get(f"https://coins.llama.fi/prices/current/{formatted_address}".format(formatted_address)).json()
        return int(value["coins"][formatted_address]['price'])

    def decode_approval(self,etherscan_txn):
        approver=etherscan_txn['from']
        token_address=etherscan_txn['to']
        input_data=etherscan_txn['input']
        spender=input_data[34:74]
        amount=int(input_data[74:],16)
        return {'approver':approver,'token_address':token_address,'spender':spender,'amount':amount}

    def is_externally_owned_account(self,address):
        code=self.web3.eth.get_code(self.web3.to_checksum_address(address)).hex()
        return code=="0x"

    def get_concurrent_approvals_on_token(self,your_address,token_address):
        payload=f"https://api.etherscan.io/api?module=account&sort=desc&action=txlist&address={your_address}&apikey={self.etherscan_api_key}"
        txns=requests.get(payload).json()['result']
        spenders=[]
        for txn in txns:
            if txn['isError']=="1":
                continue
            if txn['to']!=token_address:
                continue
            if txn['functionName']!='approve(address _spender, uint256 _value)':
                continue
            spender=self.decode_approval(txn)["spender"].lower()
            if spender in spenders:
                continue
            spenders.append(spender)
        return {'spenders':spenders,'concurrent_approvals':len(spenders)}

    def get_concurrent_approval_all(self,your_address):
        payload=f"https://api.etherscan.io/api?module=account&action=txlist&sort=desc&address={your_address}&apikey={self.etherscan_api_key}"
        txns=requests.get(payload).json()['result']
        spenders=[]
        for txn in txns:
            if txn['isError']=="1":
                continue
            if txn['functionName']!='approve(address _spender, uint256 _value)':
                continue
            spender=self.decode_approval(txn)["spender"].lower()
            if spender in spenders:
                continue
            spenders.append(spender)
        return {'spenders':spenders,'concurrent_approvals':len(spenders)}

    def get_cumulative_approval_amount_on_token(self,your_address,token_address,in_usd):
        payload=f"https://api.etherscan.io/api?module=account&sort=desc&action=txlist&address={your_address}&apikey={self.etherscan_api_key}"
        txns=requests.get(payload).json()['result']
        spenders=[]
        amount=0
        if in_usd:
            usd_value=self.get_usd_value(token_address)
        else:
            usd_value=1

        for txn in txns:
            if txn['isError']=="1":
                continue
            if txn['to']!=token_address:
                continue
            if txn['functionName']!='approve(address _spender, uint256 _value)':
                continue
            decoded=self.decode_approval(txn)
            spender=decoded["spender"].lower()
            if spender in spenders:
                continue
            spenders.append(spender)
            amount+=decoded['amount']
        return {'spenders':spenders,'amount':amount*usd_value}

    def get_cumulative_approval_amount_usd(self,your_address):
        #I've only built this function with only usd value to have continuity over all assets
        payload=f"https://api.etherscan.io/api?module=account&action=txlist&sort=desc&address={your_address}&apikey={self.etherscan_api_key}"
        txns=requests.get(payload).json()['result']
        unique_approvals={}
        amount=0
        for txn in txns:
            if txn['isError']=="1":
                continue
            if txn['functionName']!='approve(address _spender, uint256 _value)':
                continue
            decoded=self.decode_approval(txn)
            spender=decoded["spender"].lower()

            if txn['to'] in unique_approvals.keys() and spender in unique_approvals[txn['to']]:
                continue
            if txn['to'] in unique_approvals.keys():
                unique_approvals[txn['to']].append(spender)
            else:
                unique_approvals[txn['to']]=[spender]
            amount+=decoded['amount']*self.get_usd_value(txn['to'])
        return {'token_approvals':unique_approvals,'amount':amount}