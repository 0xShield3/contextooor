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

## How 2 context
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
