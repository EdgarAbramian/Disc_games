import random

'''         probability
   if the user has chosen heads then the 
   probability of getting heads will be 0.2 
   COEFF sets the probability
   flip makes a decision('H' or 'T') based on COEFF
        '''
COEFF = lambda user_coin :  0.2 if(user_coin == 'head')  else 0.8

flip = lambda user_coin: 'head' if random.random() < COEFF(user_coin = user_coin) else 'tail'
