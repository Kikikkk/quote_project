import random
from .models import Quote

def get_random_quote():
    quotes = list(Quote.objects.all())
    if not quotes:
        return None

    total_weight = sum(q.weight for q in quotes)
    r = random.uniform(0, total_weight)
    upto = 0
    for quote in quotes:
        if upto + quote.weight >= r:
            return quote
        upto += quote.weight
    return quotes[-1]
