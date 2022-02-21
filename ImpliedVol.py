"""
Created on Sun Feb 20 21:31:53 2022

@author: udaytalwar
"""
import scipy.stats as stats
import math as m 

def d(S, K, sigma, r, t):
    
    '''
    S = Current Price
    K = Strike Price
    sigma = Volatility
    r = annualized risk-free rate
    t = time to expiration
    
    returns d1, d2 for option price calculation using Black Scholes
    '''
    d1 = (m.log(S/K) + (r + (sigma**2/2))*t) * (1/(sigma*m.sqrt(t)))
    
    d2 = d1 - sigma*m.sqrt(t)
    
    return d1, d2

def option_price(S, K, sigma, r, t, flag, d1 = 0, d2 = 0):
    
    '''
    S = Current Price
    K = Strike Price
    sigma = Volatility
    r = annualized risk-free rate
    t = time to expiration
    flag = 'Call' or 'Put'
    
    returns option price according to Black Scholes
    '''
    
    if d1 == 0 and d2 == 0:
    
        d1, d2 = d(S, K, sigma, r, t)
        
        if flag == 'Call':
            
            price = stats.norm.cdf(d1)*S - stats.norm.cdf(d2)*K*m.exp(-r*t)
            
        elif flag == 'Put':
            
            price = stats.norm.cdf(-d2)*K*m.exp(-r*t) - stats.norm.cdf(-d1)*S
            
        return price 

    else: 
        
        if flag == 'Call':
            
            price = stats.norm.cdf(d1)*S - stats.norm.cdf(d2)*K*m.exp(-r*t)
            
        elif flag == 'Put':
            
            price = stats.norm.cdf(-d2)*K*m.exp(-r*t) - stats.norm.cdf(-d1)*S
            
        return price  
    
    
def imp_vol(S, K, r, t, flag, option_CMP):
    
    '''
    S = Current Price
    K = Strike Price
    r = annualized risk-free rate
    t = time to expiration
    flag = 'Call' or 'Put'
    option_CMP = current market price of option
    
    returns implied volatility of option according to Black Scholes  
    '''
    
    lb = -2  #lower bound of midpoint method
    
    ub = 5  #upper bound of midpoint method
    
    error = 1e-15  #error tolerance
    
        #midpoint method

    while (ub-lb) > error:
    
        if option_price(S, K, (ub+lb)/2, r, t, flag) - option_CMP > 0:
            ub = (lb+ub)/2
            
        else:
            lb = (lb+ub)/2
        
    return lb