import requests
from eth_uniswap import Snippets
from web3 import Web3
import random

class Tests:
    def __init__(self,w3=Web3(Web3.HTTPProvider("https://cloudflare-eth.com/"))):
        self.web3=w3
        self.uni=Snippets(self.web3,suppress_errors=True)
        self.address_targets=self.uni.SUPPORTED_CONTRACTS.keys()
        self.slippage=self.uni.getSlippage
        self.volatility=self.uni.getVolatility

    def get_transactions_by_addresses(self,addresses,depth,api_key="VP84ZNW3VHQ2S9JHE92VYXV96NX9E5U3VU"):
        big_tx=[]
        for address in addresses:
            url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}&page=1&offset={depth}"
            response = requests.get(url)
            data = response.json()
            if data['status'] != '1':
                raise ValueError('Error:', data['message'])

            transactions = data['result']
            big_tx.extend(transactions)
        random.shuffle(big_tx)
        return big_tx
    
    def expected_result(self,tx):
        data=self.uni.SUPPORTED_CONTRACTS[tx['to']]
        if tx['input'][0:10] in data['SUPPORTED_METHODS']:
            volatility='volatility_function' in data.keys()
            slippage='slippage_function' in data.keys()
        else: 
            volatility=False
            slippage=False
        return {'volatility':volatility,'slippage':slippage,'method':tx['input'][0:10],'name':data['name']}


    def test_transactions(self):
        transactions=self.get_transactions_by_addresses(self.address_targets,1000)
        for tx in transactions:
            print(tx['hash'])
            tx['to']=self.web3.to_checksum_address(tx["to"])
            expected_result=self.expected_result(tx)
            slippage=self.slippage(tx["to"],tx["input"],tx["value"])
            slippage_is_err=slippage==None
            print("slippage:",slippage,expected_result['slippage'])
            if "volatility_function" in self.uni.SUPPORTED_CONTRACTS[tx["to"]].keys():
                volatility=self.volatility(tx['to'],tx['input'])
                print("volatility:",volatility,expected_result['volatility'])
            print(expected_result)
            print("_____________________________________")


Tests().test_transactions()