import hashlib
import json
import os
import time
import logging

class BlockChain():

    def __init__(self, poll_dirname='/blocks', poll_filename='/blocks.json', logdir='logs'):
        # TODO: logs must insist poll title.

        if(logdir not in os.listdir()):
            os.mkdir(os.curdir + '/' + logdir)

        logging.basicConfig(filename=logdir+"/blockchain.log", level=0,
                            format='%(levelname)s:%(asctime)s:%(message)s')

        if(not poll_dirname.startswith('/')):
            poll_dirname = '/' + poll_dirname

        if(not poll_filename.startswith('/')):
            poll_filename = '/' + poll_filename
        
        if(not poll_filename.endswith('.json')):
            poll_filename += '.json'
    
        self.BLOCK_DIR = poll_dirname
        self.BLOCK_FILENAME = os.curdir + poll_dirname + poll_filename
    
        self.block = {'title' : '',
            'vote_for' : '',
            'prev_hash' : '',
            'timestamp' : '',
            # 'proof' : -1,
            'index' : 0
            }

        # block writes in blocks_frame in 'blocks'. 
        # There is no need to find cur_block_index, because we write 'blocks_count'
        self.blocks_frame = {
        'blocks' : [],
        'blocks_count' : 0
        }

        logging.info('Created object with poll_dirname: ' + poll_dirname + 
                    '; poll_filename: ' + poll_filename)

    def check_path():
        # TODO: code refactoring, checking begining of path (/ must be)
        return 0

    def creat_genesis_block(self):
        files = os.listdir()
        if(self.BLOCK_DIR[1:] not in files):
            os.mkdir(os.curdir + self.BLOCK_DIR)
            self.add_block()
            logging.info('Created Genesis block in ' + self.BLOCK_FILENAME)

    def get_cur_block():
        # Если выйти из программы то следующие блоки все перепишут.
        # Нужно сохранят пред. состояние
        pass

    def add_block(self, title='Genesis block', vote_for=''):
        block = self.block
        block['title'] = title
        block['vote_for'] = vote_for
        block['timestamp'] = time.time()
        block['index'] = self.blocks_frame['blocks_count']
        index = self.blocks_frame['blocks_count']
        if(index != 0):
            block['prev_hash'] = self.get_block_hash(self.blocks_frame['blocks'][index-1])

        self.blocks_frame['blocks'].append(block)
        self.blocks_frame['blocks_count'] = self.blocks_frame['blocks_count'] + 1
        print(self.blocks_frame)

        with open(self.BLOCK_FILENAME, 'w') as file:
            json.dump(self.blocks_frame, file, indent=4, ensure_ascii=False)
            logging.debug('Created block with index' + str(self.blocks_frame['blocks_count'] - 1))

    def get_block_hash(self, block):
        try:
            return hashlib.sha256(json.dumps(block).encode()).hexdigest()
        except Exception as e:
            logging.error('Block ' + ' does not exist!' + e)

    def check_blocks_integrity(self):
        return 0

if __name__ == '__main__':
    b = BlockChain()
    b.creat_genesis_block()
    b.add_block("LOL", "KEK")
    b.add_block('Lil', "Pump")

