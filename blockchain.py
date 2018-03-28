import hashlib
import json
import os
import time
import logging

class BlockChain():
    def __init__(self):
        self.BLOCK_FILENAME = os.curdir + '/blocks/blocks.json'
        logging.basicConfig(filename="log/blockchain.log", level=logging.DEBUG,
                            format='%(asctime)s:%(levelname)s:%(message)s')
        self.data = {'title' : '',
            'vote_for' : '',
            'prev_hash' : '',
            'timestamp' : '',
            'proof' : -1,
            'index' : ''
            }

    @classmethod
    def creat_block(cls):
        os.mkdir(os.curdir + "/blocks")
        return cls

    def add_block(self, title, vote_for):
        
        with open(self.BLOCK_FILENAME, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_block_hash(self, index):
        try:
            with open(self.BLOCK_FILENAME, 'rb') as file:
                return hashlib.sha256(file.read()).hexdigest()
        except Exception as e:
            logging.ERROR('File "'+file_name+'" does not exist!n', e)

    def get_next_index():
        return 0    

if __name__ == '__main__':
    b = BlockChain()