class SafeMath:

    def __init__(self):
        pass

    def standard_dev(self,list_):
        length=len(list_)
        total=total(list_)
        xbar=total/length
        sumsqr=0
        for num in list_:
            sumsqr+=(num-xbar)**2
        return (sumsqr/length)**0.5

    def safe_division(self,numerator,denominator):
        ## SAFE MATH   
            ## inf/inf  -> evaluate normally
            ## inf/n -> inf
            ## inf/0 -> inf

            ## inf/0 -> inf
            ## n/0 -> inf
            ## 0/0 -> undefined... no trade is executed

            ## 0/inf -> evaluate normally
            ## n/inf -> 0
            
            ## 0/n -> evaluate normally
            ## 0/inf -> evaluate normally

        inf=float('inf')
        if denominator==0:
            if numerator==0:
                raise ValueError("0/0 is undefined")
            else:
                result=float('inf')
        elif numerator==inf or numerator>=inf or numerator==float('-inf') or numerator<=-inf:
            if numerator==float('inf') or numerator>=inf or numerator==float('-inf') or numerator<=-inf:
                if numerator==float('inf') or numerator>=inf:
                    numerator=inf
                else:
                    numerator=-inf
                result=float(numerator)/float(denominator)
            else:
                result=float('inf')
        else:
            result=float(numerator)/float(denominator)
        
        return result
    
    def safe_exponent(self,base,exponent):
        if exponent>=0:
            return base**exponent
        else:
            if base==0:
                return float('inf')
            else:
                return base**exponent

