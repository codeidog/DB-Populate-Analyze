from .database import create_session, create_tables, ApiContent, RoomUsers
import argparse
import random, string
import logging

def main():
    


def Get_Random_UPN(User_Length:int, Domain_Lenth:int) -> str:
    """ Will return a random user@domain of the appropiate length"""
    user = Get_Random_Letter_Digits(User_Length)
    domain = f'{Get_Random_Letter_Digits(Domain_Lenth)}.{Get_Random_Letter_Digits(Domain_Lenth)}'
    return f'{user}@{domain}'

def Get_Random_Letter_Digits(count:int) -> str:
    """Will return a mix of character of the appropriate length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k= count))

if __name__ == '__main__':
    main()