#Calculate production order quantities:
import math
def inputfloat(name):
    while True:
        value = input('Enter '+name+': ')
        try:
            return float(value)
        except:
            print('Enter a valid number pls')

annualdemand = inputfloat('Annual Demand')
setupcost = inputfloat('Setup cost')
holdingcost = inputfloat('Holding cost')
workingdays = inputfloat('Annual working days')
dailyproductionrate = inputfloat('Daily production rate')
dailydemandrate = annualdemand/workingdays

EOQ = math.sqrt((2*setupcost*annualdemand)/(holdingcost*(1-dailydemandrate/dailyproductionrate)))
print(EOQ)
