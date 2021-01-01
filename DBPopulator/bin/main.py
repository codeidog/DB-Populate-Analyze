from sqlalchemy.orm import session
from sqlalchemy import create_engine
from database import create_session, create_tables, ApiContent, RoomUsers
import argparse
from os import cpu_count
import random, string
import logging
import json
import multiprocessing
import sys

db_string = f'postgresql://dbuser:passw123@localhost/IdoTest'#f'postgresql://{db_user}:{db_pwd}@{db_server}/{db_name}'

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    stream=sys.stdout
    )

def main(config: dict):    
    pool = multiprocessing.Pool(cpu_count())
    generator = RoomGenerator(config=config)    
    pool.map(generator.run, iterable= range(config['NumberOfRooms']))




class RoomGenerator():
    def __init__(self, config: dict):        
        self.config = config        

    def run(self, test):
        engine = create_engine(db_string)
        session = create_session(engine)
        room_users_list = list()
        room_ID = Get_Random_Letter_Digits(self.config['RoomIDLength'])
        user_Count = random.randint(2, self.config['MaxUserCount'])
        local_User_Prob = self.config['LocalUserProbability'] / 100
        logging.info(f'Creating 1st local user for room {room_ID}')
        upn = Get_Random_UPN(User_Length=self.config['UsernameLength'], Domain_List=self.config['InternalDomains'])
        room_User = RoomUsers(room_id = room_ID, upn=upn)
        session.add(room_User)
        session.commit()
        room_users_list.append(upn)

        logging.info(f'Creating additonal {user_Count -1} users for room {room_ID}')
        for i in range(user_Count - 1):
            if(random.random() <= local_User_Prob):
                logging.debug(f'Creating local user for room {room_ID}')
                upn = Get_Random_UPN(User_Length=self.config['UsernameLength'], Domain_List=self.config['InternalDomains'])
            else:
                logging.debug(f'creating external user for room {room_ID}')
                upn = Get_Random_UPN(User_Length=self.config['UsernameLength'], Domain_Lenth=self.config['DomainLength'])
            
            room_User = RoomUsers(room_id = room_ID, upn=upn)
            session.add(room_User)
            session.commit()
            room_users_list.append(upn)       
        roomMessages = self.Generate_Messgaes(roomID= room_ID, users_list= room_users_list, session=session)        
        session.close()
        engine.dispose()
    
    def Generate_Messgaes(self, roomID:str, users_list:list, session: session.Session) -> list:
        messageCount = self.config['NumberOfMessages']
        messages_list = list()
        logging.debug(f'Messgae count for room {roomID}:{messageCount}')
        for i in range(messageCount):
            logging.debug(f'Creating {i+1} message in room {roomID}')
            randomUser = random.choice(users_list)
            random_message = Get_Random_Letter_Digits(20)
            content = json.dumps({
                "Room": roomID,
                "Email":randomUser,
                "Message": random_message
            })
            api_Content = ApiContent(content= content)
            session.add(api_Content)
            session.commit()
        return messages_list

def Get_Random_UPN(User_Length:int, Domain_Lenth:int = None, Domain_List:list = None) -> str:
    """ Will return a random user@domain of the appropiate length, will choost a random domain from if provided"""
    user = Get_Random_Letter_Digits(User_Length)
    #Set random domain if list not set
    domain = f'{Get_Random_Letter_Digits(Domain_Lenth)}.{Get_Random_Letter_Digits(Domain_Lenth)}'\
    if Domain_List is None else random.choice(Domain_List)
    return f'{user}@{domain}'

def Get_Random_Letter_Digits(count:int) -> str:
    """Will return a mix of character of the appropriate length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k= count))

if __name__ == '__main__':
    #Parse commandline args
    parser = argparse.ArgumentParser(description='Tool to populate the tables requried for Webex')
    parser.add_argument("--config", const=True, default='config.json', nargs='?', help="The path to the JSON configuration file")    
    args = parser.parse_args()

    #Read config and load it
    configText = ''
    with open(args.config, 'r') as f:
        configText = f.read()
    config = json.loads(configText)

    #Create the required table from the database.py file
    engine = create_engine(db_string)
    create_tables(engine)
    engine.dispose()    
    main(config)