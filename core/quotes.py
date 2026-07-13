import random

QUOTES = [
    "~ Reality is just another system to analyze ~",
    "~ Built by curiosity, powered by code ~",
    "~ Nothing is hidden from those who seek understanding ~",
    "~ Knowledge is power, but execution is everything ~",
    "~ The quieter you become, the more you are able to hear ~",
    "~ In a world of noise, information is everything ~"
]

def get_quote():
    return random.choice(QUOTES)