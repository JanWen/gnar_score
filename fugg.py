from math import factorial

def probablity_mass_funtion(k, n, p):
    """
    The probability mass function for binomial distribution.
    """
    return (factorial(n) / (factorial(k) * factorial(n - k))) * (p ** k) * (1 - p) ** (n - k)
    #(factorial(n) / factorial(k) * factorial(n - k))

def shit(n, p):
    """
    The probability mass function for binomial distribution.
    """
    k = int((n+1)/2)
    n_k = factorial(n) / (factorial(k)*factorial(n-k))
    return n_k * (p**k) * ((1-p)**(n-k))

def bestOfFive(p):
	q = 1-p
	return p*p*p*(p*p + 5*p*q + 10*q*q)

"""
https://wismuth.com/elo/calculator.html#best_of=5&score=0-0&system=tennis-men&e_score=0.6
check ource calculator.js
function bestOf3(p) {
	var q = 1-p;
	return p*p*(p + 3*q);
}

function bestOf5(p) {
	var q = 1-p;
	return p*p*p*(p*p + 5*p*q + 10*q*q);
}

function bestOf7(p) {
	var q = 1-p;
	return p*p*p*p*(p*p*p + 7*p*p*q + 21*p*q*q + 35*q*q*q);
}

"""
print(
    bestOfFive(0.6)
)