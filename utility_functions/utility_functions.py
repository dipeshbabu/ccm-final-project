import math

def linear_utility(initial_bankroll, current_bankroll):
    """
    Linear utility function. Assumes utility is directly proportional to the bankroll.
    """
    return current_bankroll/initial_bankroll


def logarithmic_utility(initial_bankroll, current_bankroll):
    """
    Logarithmic utility function. Models risk aversion.
    Utility grows logarithmically with current bankroll.
    """
    if current_bankroll <= 0:
        return float('-inf')  # Log is undefined for non-positive values
    return math.log(current_bankroll / initial_bankroll)


def exponential_utility(initial_bankroll, current_bankroll, risk_aversion_coefficient=0.1):
    """
    Exponential utility function. Models risk-averse or risk-seeking behavior.
    Risk-aversion is controlled by `risk_aversion_coefficient`:
    - Positive values indicate risk aversion.
    - Negative values indicate risk-seeking behavior.
    """
    return -math.exp(-risk_aversion_coefficient * (current_bankroll - initial_bankroll))


def quadratic_utility(initial_bankroll, current_bankroll):
    """
    Quadratic utility function. Models risk-seeking behavior.
    Utility grows quadratically with current bankroll.
    """
    return (current_bankroll/initial_bankroll)**2

def quartic_utility(initial_bankroll, current_bankroll):
    """
    Quartic utility function. Models risk-seeking behavior.
    Utility grows quadratically with current bankroll.
    """
    return (current_bankroll/initial_bankroll)**4


def get_utility_function_str(utility_function):
    """
    Returns a string representation of the utility function.
    """
    if utility_function == linear_utility:
        return 'linear'
    
    elif utility_function == logarithmic_utility:
        return 'logarithmic'
    
    elif utility_function == exponential_utility:
        return 'exponential'
    
    elif utility_function == quadratic_utility:
        return 'quadratic'
    
    elif utility_function == quartic_utility:
        return 'quartic'