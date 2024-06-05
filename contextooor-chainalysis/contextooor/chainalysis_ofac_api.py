import requests
import os

chainalysis_api_url = "https://public.chainalysis.com/api/v1/address/"

DEMO_SANCTIONED_ADDRESSES=["1JHdQHkBZiim1cb4hyUh2PbzEbbg6z2Trf", "0x01e2919679362dFBC9ee1644Ba9C6da6D6245BB1"]

DEMO_NON_SANCTIONED_ADDRESSES=["bc1p7pztjz9qyupr8ztwqy2y3yl7u6y2nvfna3g54rq3s3d7d0k5ee4syceevj", "0x01B2f8877f3e8F366eF4D4F48230949123733897"]

class Chainalysis:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_address_sanction_status(self, address):
        url = chainalysis_api_url + address
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': self.api_key
        }
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def is_sanctioned(self, address):
        result = self.get_address_sanction_status(address)
        return len(result['identifications']) > 0
        
    def check_sanctioned_addresses(self, addresses):
        sanctioned_addresses = []
        for address in addresses:
            if self.is_sanctioned(address):
                sanctioned_addresses.append(address)
        return sanctioned_addresses
        
    def get_sanctioned_address_data(self, address):
        result = self.get_address_sanction_status(address)
        return result['identifications']

def test_chainalysis():
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

