from math import ceil
from timeit import default_timer as timer
from colorama import Fore, Back

def geometric_increase(base, rate, exponent):
    return(base * rate ** exponent)


commas = "{:,}"

def first(mana):
    level = 0
    geo = 0
    sum = 0
    for i in range(100000):
        geo = 1.008**i
        if sum + geo <= mana:
            sum += ceil(geo)
            level += 1
        else:
            break
        print('level: ' + str(level), 'used: ' + str(sum), sep=' ||| ')
    print(level, ceil(geo), f'{sum}/{mana}', sep=" ||| ")

def second(mana):
    level = 0
    mana_to_next_level = 0
    total_mana_used = 0
    while True:
        mana_to_next_level = ceil(1.008 ** level)
        if total_mana_used + mana_to_next_level  <= mana:
            total_mana_used += mana_to_next_level
            level += 1
        else:
            print(level, mana_to_next_level, f'{total_mana_used}/{mana}', sep=' ||| ')
            break



def test_sum():
    try:
        assert sum((1,2)) == 3
        print(Back.GREEN + 'pass'+Back.RESET)
    except:
        print(Fore.RED + 'failed' + Fore.RESET)


start = timer()
test_sum()
finish = timer()
print(finish - start)