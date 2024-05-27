from web3 import Web3
import requests
import json
import subprocess
import os
import polars as pl
from contextooor.core.Chainalysis.chainalysis_ofac_api import Chainalysis

DEMO_SANCTIONED_ADDRESSES=["1JHdQHkBZiim1cb4hyUh2PbzEbbg6z2Trf", "0x01e2919679362dFBC9ee1644Ba9C6da6D6245BB1"]

DEMO_NON_SANCTIONED_ADDRESSES=["bc1p7pztjz9qyupr8ztwqy2y3yl7u6y2nvfna3g54rq3s3d7d0k5ee4syceevj", "0x01B2f8877f3e8F366eF4D4F48230949123733897"]

class Snippets:

    def __init__(self,w3=Web3(Web3.HTTPProvider("https://eth.public-rpc.com")),etherscan_api_key="PGJ5AYE9WGD77YPS4F3NGQ33MB5YI7JYS8"):
        self.etherscan_api_key=etherscan_api_key
        self.web3=w3
        try:
            self.web3.eth.get_block_number()
        except Exception:
            self.web3=Web3(Web3.HTTPProvider("https://eth.public-rpc.com"))
        self.v2_pair_abi="""[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]"""

    def is_known_attacker(self,forta_api_key,address):
        ## The api key should be in the format you get from forta ex: keyname:api_key
        headers = {
            'content-type': 'application/json',
            'Authorization': f'bearer {forta_api_key}'}
        data = """{"query":"query Labels($input: LabelsInput) {\\n  labels(input: $input) {\\n    labels {\\n      id\\n      label {\\n        entity\\n        entityType\\n        label\\n      }\\n      source {\\n        id\\n      }\\n    }\\n  }\\n}","variables":{"input":{"entities":"""+'"'+address+'"'+""","labels":["attacker-contract","attacker-eoa"],"sourceIds":"0x80ed808b586aeebe9cdd4088ea4dea0a8e322909c0e4493c993e060e89c09ed1"}}}"""
        response = requests.post('https://api.forta.network/graphql', headers=headers, data=data)
        response=response.json()
        if response['data']['labels']['labels']!=[]:
            return True
        return False
        
    def is_sanctioned(self,chainalysis_api_key,address):
        chainalysis = Chainalysis(chainalysis_api_key)
        is_sanctioned = chainalysis.is_sanctioned(address)
        return is_sanctioned

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
    
    def get_audit(self,address,summarize=True):
        current_directory = os.getcwd()
        command = ["slither", address, "--json", "-"]

        result = subprocess.run(command, capture_output=True, text=True,cwd=current_directory)
        print(result.stdout)
        data=json.loads(result.stdout)
        if summarize==False:
            return data
        parsed_results = []
        summary={}

        for detector in data.get("results", {}).get("detectors", []):

            check = detector.get("check", "")
            impact = detector.get("impact", "").capitalize()
            if impact in summary.keys():
                summary[impact]+=1
            else:
                summary[impact]=1

            confidence = detector.get("confidence", "").capitalize()
            
            # Append the extracted information to the results list
            parsed_results.append({
                "check": check,
                "impact": impact,
                "confidence": confidence
            })
        return {"summary":summary,"results":parsed_results}
    
    def get_normal_tx_history(self,from_address,api_key,current_block_number):
        url = "https://api.etherscan.io/api"
        params = {
            "module": "account",
            "action": "txlist",
            "address": from_address,
            "startblock": 0,
            "endblock": current_block_number-1,
            "sort": "asc",
            "apikey": api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            transactions = response.json()
            return transactions['result']
        else:
            return "Error: Unable to fetch transactions"

    def get_token_tx_history(self,from_address,api_key,current_block_number):
        url = "https://api.etherscan.io/api"
        params = {
            "module": "account",
            "action": "tokentx",
            "address": from_address,
            "startblock": 0,
            "endblock": current_block_number-1,
            "sort": "asc",
            "apikey": api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            transactions = response.json()
            return transactions['result']
        else:
            return "Error: Unable to fetch transactions"

    def get_tx_history(self,from_address,current_block_number):
        norm=self.get_normal_tx_history(from_address,self.etherscan_api_key,current_block_number)
        token=self.get_token_tx_history(from_address,self.etherscan_api_key,current_block_number)
        df_norm=pl.DataFrame(norm).select('from','to','gasUsed','blockNumber')
        df_token=pl.DataFrame(token).select('from','to','gasUsed','blockNumber')
        return pl.concat([df_norm,df_token]).lazy()

    def find_matches(self,df, from_address, to_address, first_n, last_n):
        original_df=df
        combined_list=\
            pl.concat([df.select(pl.col.to),df.select(pl.col('from')).rename({'from':'to'})])\
            .unique()\
            .rename({'to':'address'})\
            .filter(pl.col.address!=from_address)\
            .with_columns(
                match=
                pl.when(pl.col.address==to_address).then(pl.lit("exact_match")).otherwise(
                pl.when(pl.col.address.str.starts_with(to_address[0:first_n+2]) & pl.col.address.str.ends_with(to_address[-last_n:]))\
                    .then(pl.lit("both"))\
                    .otherwise(
                        pl.when(pl.col.address.str.starts_with(to_address[0:first_n+2]))\
                        .then(pl.lit('start'))
                        .otherwise(
                            pl.when(pl.col.address.str.ends_with(to_address[-last_n:]))
                            .then(pl.lit('end'))
                            .otherwise(None)
                ))))\
            .drop_nulls()\
        
        result_df=\
            pl.concat([
                original_df.select(['to','gasUsed','blockNumber'])
                    .rename({'to':'address'}),
                original_df.select(['from','gasUsed','blockNumber'])
                    .rename({'from':'address'})
                ])\
            .sort('blockNumber','gasUsed',descending=False, nulls_last=True)\
            .join(combined_list,on="address",how='left')\
            .drop_nulls()\
            .collect()   
        return result_df

    def parse_results(self,result_df,to_address):
        if result_df.shape[0]==0:
            previous_interactions=False
            previous_phishing_attempts=False
            phishing_likely=False
        else:
            different_addresses=result_df.select(pl.col.address).n_unique()
            first_result=result_df.select(pl.col.match).head(1).item()
            previous_phishing_attempts=different_addresses!=1
            previous_interactions=to_address in result_df['address']
            if first_result=="exact_match":
                phishing_likely=False
            if first_result!="exact_match":
                phishing_likely=True
        return {"to-address-phishing-likely":phishing_likely, "previously-targetted-to-address":previous_phishing_attempts, "previous-interactions-with-to-address":previous_interactions}

    def is_poisonned_address(self,from_address,to_address, first_n=4, last_n=4, current_block_number=99999999):
        from_address=from_address.lower()
        to_address=to_address.lower()
        df=self.get_tx_history(from_address,current_block_number)
        matchbook=self.find_matches(df,from_address,to_address,first_n,last_n)
        return self.parse_results(matchbook,to_address)
    
def test_snippets():
    api_key = os.getenv('CHAINALYSIS_API_KEY')
    if api_key is None:
        raise ValueError("CHAINALYSIS_API_KEY is not set")

    chainalysis = Chainalysis(api_key)
    for address in DEMO_SANCTIONED_ADDRESSES:
      is_sanctioned = chainalysis.is_sanctioned(address)
      assert is_sanctioned == True
      
      sanction_data = chainalysis.get_sanctioned_address_data(address)
      assert sanction_data[0]["category"] == "sanctioned entity"
      
    for address in DEMO_NON_SANCTIONED_ADDRESSES:
      is_sanctioned = chainalysis.is_sanctioned(address)
      assert is_sanctioned == False

      sanction_data = chainalysis.get_sanctioned_address_data(address)
      assert len(sanction_data) == 0

