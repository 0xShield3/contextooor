from contextooor.core.universal_router.V3_universal_router import UniswapV3
from contextooor.core.universal_router.V2_universal_router import UniswapV2
from uniswap_universal_router_decoder import RouterCodec
import re

class Data:

    def __init__(self):
        self.SUPPORTED_FUNCTIONS = {
            'V2_SWAP_EXACT_IN': UniswapV2(),
            'V2_SWAP_EXACT_OUT': UniswapV2(),
            'V3_SWAP_EXACT_IN': UniswapV3(),
            'V3_SWAP_EXACT_OUT': UniswapV3(),
        }

        self.SUPPORTED_METHODS=['0x3593564c']

    def get_bridge_routes(self,data):
        bridge_routes=[]
        all_items=[]
        for i in range(0,len(data)-1):
            ## check recipient, if it is a valid address, this means this route is the sender in a bridged route.
            if data[i][1]['recipient'] in ["0x0000000000000000000000000000000000000001","0x0000000000000000000000000000000000000002"]:
                continue
            ## set sender idx
            from_idx=i
            ## loop through routes to find receiver
            for j in range(0,len(data)):
                if list(data[j][2].keys())[0]==data[i][1]['recipient']:
                    to_idx=j
                    break

            ##check if sender is already part of a known bridged route, insert if it is
            if from_idx in all_items:
                for routes in bridge_routes:
                    if from_idx in routes:
                        insert_at=routes.index(from_idx)+1
                        routes.insert(insert_at,to_idx)
                        break
            else:
                all_items.append(from_idx)
                if to_idx not in all_items:
                    all_items.append(to_idx)
                bridge_routes.append([from_idx,to_idx])
        return bridge_routes,all_items
    
    def get_easy_slippage(self,web3,data,amount_in=None,block="latest"):
        uniswap=self.SUPPORTED_FUNCTIONS[data[0]]
        result=uniswap.get_max_slippage(web3,data,amount_in,block)
        return result

    def process_bridge_routes(self,web3,data,bridge_routes,block):
        returnable_list=[]
        for route in bridge_routes:
            running_unslippage=1
            amount_in=None
            for idx,inner_route in enumerate(route):
                this_route_data=data[inner_route]
                slippage_dict=self.get_easy_slippage(web3,this_route_data,amount_in=amount_in,block=block)
                amount_in=slippage_dict['amount_out']
                if idx == 0:
                    in_token=slippage_dict['in_token']
                    amount_in0=slippage_dict['amount_in']
                unslippage=(slippage_dict['slippage']-1)*-1
                running_unslippage=running_unslippage*unslippage
            slippage=1-running_unslippage
            returnable_list.append({'slippage':slippage,'amount_out':slippage_dict['amount_out'],'amount_in':amount_in0,'in_token':in_token,'out_token':slippage_dict['out_token']})
        return returnable_list

    def path_decode_conditional(self, codec, decoded_data):
        decoded_input_data=decoded_data[1]
        if decoded_data[0][0:2]=="V3":
            decoded_path=list(codec.decode.v3_path(decoded_data[0],decoded_input_data['path']))
            decoded_input_data['path']=decoded_path
        return [decoded_data[0],decoded_input_data]

    def tabulate_weighted_slippage(self,total_amount,slippage_amt_list):
        slippage=0
        for lst in slippage_amt_list:
            slippage+=lst[0]*(lst[1]/total_amount)
        return slippage

    def validate_MPR_Assmp(self,in_token_list,out_token_list):
        print('validating')
        in_list=len(list(set(in_token_list)))==1
        out_list=len(list(set(out_token_list)))==1
        return in_list and out_list

    def extract_data(self,trx_input):
        codec = RouterCodec()
        returnable=[]
        decoded_trx_input = codec.decode.function_input(trx_input)
        for i in decoded_trx_input[1]['inputs']:

            fn_name=re.search('<Function (.*?)\(', str(i[0]))
            if fn_name==None:
                continue

            fn_name=fn_name.group(1)

            if fn_name not in self.SUPPORTED_FUNCTIONS.keys():
                continue

            returnable.append(self.path_decode_conditional(codec,[fn_name,i[1]]))

        return returnable

    def get_unique_in_tokens(self,slippage_dict):
        returnable=[]
        for slip in slippage_dict:
            returnable.append(slip['in_token'])
        return returnable
    
    def get_total_and_max_for_token(self,slippage_dict,token):
        total=0
        max_slippage=-2**256
        for slip in slippage_dict:
            if slip['in_token']==token:
                total+=slip['amount_in']
                if slip['slippage']>max_slippage:
                    max_slippage=slip['slippage']
        return total,max_slippage

    def get_potential_slippage(self,web3,trx_input,block):
        method_name=trx_input[0:10]
        
        if  method_name not in self.SUPPORTED_METHODS:
            raise ValueError(f'Unsupported Method: {method_name}')
        
        prepped_data=self.extract_data(trx_input)
        data_with_routes=[]
        for route in prepped_data:
            uniswap=self.SUPPORTED_FUNCTIONS[route[0]]
            pool_planner=uniswap.get_pool_planner(route)
            pair_route=uniswap.getPoolAddresses(web3,pool_planner)
            data_with_routes.append([route[0],route[1],pair_route])
        bridge_routes,flat_list=self.get_bridge_routes(data_with_routes)
        results=self.process_bridge_routes(web3,data_with_routes,bridge_routes,block)
        for j,k in enumerate(data_with_routes):
            if j in flat_list:
                continue
            deez_results=self.get_easy_slippage(web3,data=k,block=block)
            results.append(deez_results)
        unique_in_tokens= self.get_unique_in_tokens(results)
        aggregate_results={}
        for token in unique_in_tokens:
            total,max_slippage=self.get_total_and_max_for_token(results,token)
            weighted_slippage=0
            deez_slippages=[]
            for slip in results:
                if slip['in_token']==token:
                    weighted_slippage+=(slip['slippage']*slip['amount_in'])/total
                    deez_slippages.append(slip)
            aggregate_results[token]={'weighted_slippage':weighted_slippage,'max_slippage':max_slippage,'routes':deez_slippages}
        return aggregate_results


       
       
       
       
       
       
       
       
       
       
       
        # if len(prepped_data)<=1:
        #     function_to_call=self.SUPPORTED_FUNCTIONS[prepped_data[0][0]]
        #     slippage_amt,_,_=function_to_call(web3,prepped_data[0])
        #     return slippage_amt[0]
        
        # in_token_list=[]
        # out_token_list=[]
        # slippage_amt_list=[]
        # running_total=0
        # for data in prepped_data:
        #     function_to_call=self.SUPPORTED_FUNCTIONS[data[0]]
        #     slippage_amt,in_token,out_token=function_to_call.get_max_slippage(web3,data)
        #     in_token_list.append(in_token)
        #     out_token_list.append(out_token)
        #     slippage_amt_list.append(slippage_amt)
        #     running_total+=slippage_amt[1]
        
        # if not self.validate_MPR_Assmp(in_token_list,out_token_list):
        #     return "MPR ERROR: ASSUMPTION NOT TRUE"
        
        # return self.tabulate_weighted_slippage(running_total,slippage_amt_list)