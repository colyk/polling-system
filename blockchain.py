import hashlib
import json
import os
import time
import logging

class BlockChain():

    def __init__(self, dir_name='/blocks', poll_name='/blocks.json'):
        logging.basicConfig(filename="log/blockchain.log", level=0,
                            format='%(levelname)s:%(asctime)s:%(message)s')

        if(not dir_name.startswith('/')):
            dir_name = '/' + dir_name

        if(not poll_name.startswith('/')):
            poll_name = '/' + poll_name
        
        if(not poll_name.endswith('.json')):
            poll_name += '.json'
    
        self.BLOCK_DIR = dir_name
        self.BLOCK_FILENAME = os.curdir + dir_name + poll_name
    
        self.block = {'title' : '',
            'vote_for' : '',
            'prev_hash' : '',
            'timestamp' : '',
            'proof' : -1,
            'index' : 0
            }

        # block writes in blocks_frame in 'blocks'. 
        # There is no need to find cur_block_index, because we write 'blocks_count'
        self.blocks_frame = {
        'blocks' : [],
        'blocks_count' : 0
        }

        logging.info('Created object with dir_name: ' + dir_name + 
                    '; poll_name: ' + poll_name)

    def creat_genesis_block(self):
        files = os.listdir(os.curdir)
        if(self.BLOCK_DIR[1:] not in files):
            os.mkdir(os.curdir + self.BLOCK_DIR)
            self.add_block()
            logging.info('Created Genesis block in ' + self.BLOCK_FILENAME)

    def add_block(self, title='Genesis block', vote_for=''):
        # TODO: put block into blocks_frame
        block = self.block
        block['title'] = title
        block['vote_for'] = vote_for
        block['timestamp'] = time.time()

        with open(self.BLOCK_FILENAME, 'w') as file:
            json.dump(block, file, indent=4, ensure_ascii=False)
            logging.debug('Created block with index' + block['index'])

    def get_block_hash(self, index):
        try:
            with open(self.BLOCK_FILENAME, 'rb') as file:
                return hashlib.sha256(file.read()).hexdigest()
        except Exception as e:
            logging.error('Block ' + index + ' does not exist!' + e)

    def check_blocks_integrity():
        return 0

if __name__ == '__main__':
    b = BlockChain()
    b.creat_genesis_block()

