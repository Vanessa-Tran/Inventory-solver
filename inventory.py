import math
import matplotlib.pyplot as plt

# Asks the user for a boolean, and will block until a valid boolean is entered.
def inputbool(name):
    while True:
        value = input(name+'? (Y/N): ')
        if value == 'Y':
            return True
        elif value == 'N':
            return False
        else:
            print('Enter "Y" or "N" pls')

# Asks the user for a float, and will block until a valid float is entered.
def inputfloat(name):
    while True:
        value = input('Enter ' + name + ': ')
        try:
            return float(value)
        except:
            print('Enter a valid number pls')

def getDiscountCost(cost, numberofitems):
    discountcost = 0
    if numberofitems <= 150: discountcost = cost
    if numberofitems >= 151 and numberofitems <= 300: discountcost = 0.98*cost
    if numberofitems >= 301 and numberofitems <= 800: discountcost = 0.95*cost
    if numberofitems >= 801: discountcost = 0.9*cost
    return discountcost

setupcost = inputfloat('setup cost')
annualdemand = int(inputfloat('annual demand'))
basecost = inputfloat('item cost')
invtpercentage = inputfloat('inventory percentage')
leadtime = inputfloat('lead time')

isDiscount = inputbool('Enable discounts')
#Calculate replenishment level:
replenishedlevel = (annualdemand/365)*leadtime #lead (lead time) is the number of days waiting for the delivery arrival
print('replenishment level: ', replenishedlevel)

smallestInvtCost = None
optimalOrderQuantity = 0
optimalHoldingCost = 0
optimalEoq = 0
optimalOpy = 0
optimalDbo = 0
optimalAPC = 0
optimalAOC = 0
optimalAHC = 0
quantitylst = list()
totalinvtcostlst = list()
holdingcostlst = list()
for quantity in range(1,annualdemand):
    if isDiscount:
        productcost = getDiscountCost(basecost, quantity)
    else:
        productcost = basecost
    holdingcost = productcost*invtpercentage
    #Calculate economic order quantity:
    EOQ = math.sqrt((2*setupcost*annualdemand)/holdingcost)
    #Calculate orders per year:
    opy = annualdemand/EOQ
    dbo = 365/opy
    #Determine increased cost of constrained purchases:
    ordercost = (annualdemand/quantity)*setupcost
    constrainedholdingcost = (0.5*quantity*holdingcost) #Assumption: 0.5 is the leftover inventory in the previous order
    Totalinvtcost = ordercost + constrainedholdingcost
    #print(quantity, Totalinvtcost)
    #Calculate annual indexes:
    annualproductcost = annualdemand*productcost
    annualordercost = annualproductcost/EOQ
    annualholdingcost = 0.5*EOQ*holdingcost #Assumption: 0.5 is the leftover inventory in the previous order
    total3costs = annualproductcost + annualordercost + annualholdingcost
    if smallestInvtCost is None or smallestInvtCost > Totalinvtcost:
        smallestInvtCost = Totalinvtcost
        optimalOrderQuantity = quantity
        optimalHoldingCost = holdingcost
        optimalEoq = EOQ
        optimalOpy = opy
        optimalDbo = dbo
        optimalAPC = annualproductcost
        optimalAOC = annualordercost
        optimalAHC = annualholdingcost
    if quantity%30 == 0:
        quantitylst.append(quantity)
        totalinvtcostlst.append(Totalinvtcost)
        holdingcostlst.append(constrainedholdingcost)
#print(collectlst) #tuple list (quantity,Totalinvtcost)

print("Holding cost: ", optimalHoldingCost)
print('Economic order quantity: ', optimalEoq)
print('orders per year: ', optimalOpy)
print('days between orders: ', optimalDbo)
print('Annual product cost: ', optimalAPC)
print('Annual ordering cost: ', optimalAOC)
print('Annual holding cost: ', optimalAHC)
print('Optimal total inventory cost: ', smallestInvtCost)
print('Optimal quantity: ', optimalOrderQuantity)
plt.plot(quantitylst, totalinvtcostlst, label = 'Allcost')
plt.plot(quantitylst, holdingcostlst, label = 'HoldingCost')
plt.xlabel('Quantity')
plt.ylabel('Total Cost')
plt.title('Order Optimisation')
plt.legend()
plt.show()
