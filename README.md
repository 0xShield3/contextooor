# Contextooor
A library to gather more data from your transaction before broadcasting.

``` pip install contextooor ```

## Uniswap:
    - Universal router supports execute, but missing support for the second execute method
    - Volatility and slippage on all swap methods on V2 router
    - Other than multicall, slippage and volatility on all swap methods on V3 router
    - TODO: Transactions directly to pairs, multicall on V3, second execute method on universal router, volatility on universal router, fee accounting on universal router

## Snippets:
    - Converting to USD
    - Concurrent approvals on a specific token
    - Concurrent approvals on all tokens
    - Total amount approved on a specific token (usd or token value)
    - Total amount approved on all tokens (usd)
    - Moooore 

## Bitcoin:
    - Decoding to transaction object
    - Polars dataframe of recipient and their value (aggregated by recipient)
    - Total value of transaction
    - Value sent to a specified address
    - Recipient is in OFAC Sanction list
    - Largest individual amount sent
    - Number of recipients

## How 2 context
### EVM Contexting
```Python
from contextooor.uniswap import uniswap
from contextooor.snippets import Snippets
from web3 import Web3

your_address="0x077B78B2793C956080888c4A496Ea81eCa11827F"
weth_contract="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
w3=Web3(Web3.HTTPProvider("https://your-rpc-url.com"))

##w3 is an optional variable, defaulting to public rpcs
uniswap(w3=w3).getSlippage(to_address="0x",input_data="0x",value=123)
uniswap(w3=w3).getVolatility(to_address="0x",input_data="0x")

Snippets().get_concurrent_approval_all(your_address=your_address)
Snippets().get_concurrent_approvals_on_token(your_address=your_address,token_address=weth_contract)
Snippets().get_cumulative_approval_amount_on_token(your_address=your_address,token_address=weth_contract,in_usd=True)
Snippets().get_cumulative_approval_amount_usd(your_address=your_address)
Snippets().get_usd_value(token=weth_contract)
Snippets().is_externally_owned_account(address=your_address)

```
### Bitcoin contexting
```Python
from contextooor import btc
encoded_tx="0200000..."
bitcoin=btc.BitcoinUtils(encoded_tx)

print("Contains sanctioned addresse(s)?",bitcoin.contains_sanctioned_addresses())

print("total value of transaction in satoshis",bitcoin.total_value())
print("total value of transaction in bitcoin",bitcoin.total_value(denomination="bitcoin"))

print("Largest individual transfer:",btc.max_single_transfer(denomination="bitcoin"))
print("Number of recipients:",btc.recipient_count())

print("Satoshis sent to 'bc1...':",bitcoin.value_to("bc1qdugdmvfqrq5qjlw4ta7alen2hdpsekjkjen5xw"))
print("Bitcoins sent to 'bc1...':",bitcoin.value_to("bc1qdugdmvfqrq5qjlw4ta7alen2hdpsekjkjen5xw",denomination="bitcoin"))

print("Decoded transaction object:",bitcoin.decoded_tx_obj)
print("Polars dataframe of recipient and their value (aggregated to unique addresses)",bitcoin.decoded_dataframe)


```
