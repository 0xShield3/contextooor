from web3 import Web3

class Addresses:
    def __init__(self,w3=Web3(Web3.HTTPProvider("https://eth.public-rpc.com"))):
        self.w3=w3
        self.chain=w3.eth.chain_id
        self.addresses_dict={
            #mainnet
            1:{'universal':["0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD"], #"0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B" universal router should be added
               'v2router':"0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
               'v2factory':"0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
               'v3router_1':"0xE592427A0AEce92De3Edee1F18E0157C05861564",
               'v3router_2':"0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
               'v3factory':"0x1F98431c8aD98523631AE4a59f267346ea31F984",
               'scanner':"api.etherscan.io",
               'scanner_api_key':"PGJ5AYE9WGD77YPS4F3NGQ33MB5YI7JYS8",
               'rpc':'https://eth-mainnet.g.alchemy.com/v2/gtyhfTVgRS5Yg5mkWaFmMYShFCflvKkl'},
            
            #sepolia
            11155111:{'universal':["0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD"],
                'v2router':"0x425141165d3DE9FEC831896C016617a52363b687",
                'v2factory':"0xB7f907f7A9eBC822a80BD25E224be42Ce0A698A0",
                'v3router_1':None,
                'v3router_2':"0x3bFA4769FB09eefC5a80d6E87c3B9C650f7Ae48E",
                'v3factory':"0x0227628f3F023bb0B980b67D528571c95c6DaC1c",
                'scanner':"api-sepolia.etherscan.io",
                'scanner_api_key':"PGJ5AYE9WGD77YPS4F3NGQ33MB5YI7JYS8",
                'rpc':'https://eth-sepolia.g.alchemy.com/v2/gtyhfTVgRS5Yg5mkWaFmMYShFCflvKkl'}, 

            #polygon
            137:{'universal':["0x4C60051384bd2d3C01bfc845Cf5F4b44bcbE9de5"], #"0xec7BE89e9d109e7e3Fec59c222CF297125FEFda2" universal router v1 2 v2 support should be added as well as universal router 3 "0x643770E279d5D0733F21d6DC03A8efbABf3255B4"
                'v2router':"0xedf6066a2b290C185783862C7F4776A2C8077AD1",
                'v2factory':"0x9e5A52f57b3038F1B8EeE45F28b3C1967e22799C",
                'v3router_1':"0xE592427A0AEce92De3Edee1F18E0157C05861564",
                'v3router_2':"0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
                'v3factory':"0x1F98431c8aD98523631AE4a59f267346ea31F984",
                'scanner':"api.polygonscan.com",
                'scanner_api_key':"BPPIQUAWXX11AUP312KQ6M9IQF1GX7YAN5",
                'rpc':'https://polygon.api.onfinality.io/public'},  
                    
            # 80002:{'universal':[],
            #     'v2router':[],
            #     'v2factory':[],
            #     'v3router':[],
            #     'v3factory':[]}, #polygon amoy
            #optimism
            10:{'universal':["0xb555edF5dcF85f42cEeF1f3630a52A108E55A654"], #"0xeC8B0F7Ffe3ae75d7FfAb09429e3675bb63503e4" universal router v1 2 should be added as well as "0xCb1355ff08Ab38bBCE60111F1bb2B784bE25D7e8" v1 2 v2
                'v2router':None,#v2 router 2 currently not working
                'v2factory':"0x0c3c1c532F1e39EdF36BE9Fe0bE1410313E074Bf",
                'v3router_1':"0xE592427A0AEce92De3Edee1F18E0157C05861564",
                'v3router_2':"0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
                'v3factory':"0x1F98431c8aD98523631AE4a59f267346ea31F984",
                'scanner':"api-optimistic.etherscan.io",
                'scanner_api_key':"Y6FKNCFHZ84Y74ZD49R6CT7N2VGB2EDGNT",
                'rpc':'https://optimism-rpc.publicnode.com'},
                
            # 11155420:{'universal':["0xD5bBa708b39537d33F2812E5Ea032622456F1A95"],
            #     'v2router':[],
            #     'v2factory':[],
            #     'v3router':["0x94cC0AaC535CCDB3C01d6787D6413C739ae12bc4"],
            #     'v3factory':"0x4752ba5DBc23f44D87826276BF6Fd6b1C372aD24"}, #optimism sepolia

            # 42220:{'universal':["0xC73d61d192FB994157168Fb56730FdEc64C9Cb8F","0x643770e279d5d733f21d6dc03a8efbabf3255b4"],
            #     'v2router':[],
            #     'v2factory':[],
            #     'v3router':[],
            #     'v3factory':[]}, #celo

            # 44787:{'universal':["0x4648a43B2C14Da09FdF82B161150d3F634f40491","0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD"],
            #     'v2router':[],
            #     'v2factory':[],
            #     'v3router':[],
            #     'v3factory':[]}, #celo alfajores
            
            #bsc
            56:{'universal':["0x5Dc88340E1c5c6366864Ee415d6034cadd1A9897"], #these other routers should be added "0xeC8B0F7Ffe3ae75d7FfAb09429e3675bb63503e4","0x4Dae2f939ACf50408e13d58534Ff8c2776d45265"
                'v2router':"0x4752ba5DBc23f44D87826276BF6Fd6b1C372aD24",
                'v2factory':"0x8909Dc15e40173Ff4699343b6eB8132c65e18eC6",
                'v3router_1':None,
                'v3router_2':"0xB971eF87ede563556b2ED4b1C0b0019111Dd85d2",
                'v3factory':"0xdB1d10011AD0Ff90774D0C6Bb92e5C5c8b4461F7",
                'scanner':"api.bscscan.com",
                'scanner_api_key':"3CANUWB7DPMQW1GG5AJYIXVQKRREAZPZNK",
                'rpc':'https://bsc-rpc.publicnode.com'},

            #base 
            8453:{'universal':["0xeC8B0F7Ffe3ae75d7FfAb09429e3675bb63503e4","0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD"],
                'v2router':"0x4752ba5DBc23f44D87826276BF6Fd6b1C372aD24",
                'v2factory':"0x8909Dc15e40173Ff4699343b6eB8132c65e18eC6",
                'v3router_1':None,
                'v3router_2':"0x2626664c2603336E57B271c5C0b26F421741e481",
                'v3factory':"0x33128a8fC17869897dcE68Ed026d694621f6FDfD",
                'scanner':"api.basescan.org",
                'scanner_api_key':"NRT1PZS36URXP3P7ME2SYBFG6NMD18CZT6",
                'rpc':'https://base-rpc.publicnode.com'}, 

            # 84532:{'universal':"0x050E797f3625EC8785265e1d9BDd4799b97528A1",
            #     'v2router':[],
            #     'v2factory':[],
            #     'v3router':"0x94cC0AaC535CCDB3C01d6787D6413C739ae12bc4",
            #     'v3factory':"0x4752ba5DBc23f44D87826276BF6Fd6b1C372aD24"}, #base sepolia
            
            #avalanche
            43114:{'universal':["0x82635AF6146972cD6601161c4472ffe97237D292","0x4Dae2f939ACf50408e13d58534Ff8c2776d45265"],
                'v2router':"0x4752ba5dbc23f44d87826276bf6fd6b1c372ad24",
                'v2factory':"0x9e5A52f57b3038F1B8EeE45F28b3C1967e22799C",
                'v3router_1':None,
                'v3router_2':"0xbb00FF08d01D300023C629E8fFfFcb65A5a578cE",
                'v3factory':"0x740b1c1de25031C31FF4fC9A62f554A55cdC1baD",
                'scanner':None,
                'scanner_api_key':None,
                'rpc':'https://avalanche.drpc.org'}, 

            #arbitrum one
            42161:{'universal':["0x4C60051384bd2d3C01bfc845Cf5F4b44bcbE9de5","0xeC8B0F7Ffe3ae75d7FfAb09429e3675bb63503e4","0x5E325eDA8064b456f4781070C0738d849c824258"],
                'v2router':"0x4752ba5DBc23f44D87826276BF6Fd6b1C372aD24",
                'v2factory':"0xf1D7CC64Fb4452F05c498126312eBE29f30Fbcf9",
                'v3router_1':None,
                'v3router_2':"0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
                'v3factory':"0x1F98431c8aD98523631AE4a59f267346ea31F984",
                'scanner':"api.arbiscan.io",
                'scanner_api_key':"TVGA4HW9JYJECRTG2X4QNAICG87E552H59",
                'rpc':'https://arb-mainnet.g.alchemy.com/v2/gtyhfTVgRS5Yg5mkWaFmMYShFCflvKkl'}, 

            # 421614:{'universal':["0x4A7b5Da61326A6379179b40d00F57E5bbDC962c2"],
            #     'v2router':[],
            #     'v2factory':[],
            #     'v3router':"0x101F443B4d1b059569D643917553c771E1b9663E",
            #     'v3factory':"0x248AB79Bbb9bC29bB72f7Cd42F17e054Fc40188e"}, #arbitrum sepolia
            }
        
        if self.chain not in self.addresses_dict.keys():
            raise ValueError("chain is not supported")
        
        self.addresses=self.addresses_dict[self.chain]
        self.universal=self.addresses['universal']
        self.v2router=self.addresses['v2router']
        self.v2factory=self.addresses['v2factory']
        self.v3router_1=self.addresses['v3router_1']
        self.v3router_2=self.addresses['v3router_2']
        self.v3factory=self.addresses['v3factory']

    
    def isRouter(self,address):
        address=self.w3.to_checksum_address(address)
        self.routers=[self.v2router]
        self.routers.extend(self.universal)
        self.routers.extend(self.v3router)
        return address in self.routers

    def whichRouter(self,address):
        address=self.w3.to_checksum_address(address)
        if address in self.universal:
            return 'universal_router'
        if address == self.v3router_1:
            return 'v3_router_1'
        if address == self.v3router_2:
            return 'v3_router_2'
        if address == self.v2router:
            return 'v2_router'
        return None