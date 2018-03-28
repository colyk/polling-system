import hashlib
import json
import os
import time
import logging

# TODO: refactoring!

class BlockChain():

    def __init__(self, poll_dirname='/blocks', poll_filename='/blocks.json', logdir='logs'):
        # TODO: logs must insist poll title.

        if(logdir not in os.listdir()):
            os.mkdir(os.curdir + '/' + logdir)

        logging.basicConfig(filename=logdir+"/blockchain.log", level=logging.NOTSET,
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
        self.creat_genesis_block()
        self.save_cur_block()

    def check_path():
        # TODO: code refactoring, checking begining of path (/ must be)
        pass

    def creat_genesis_block(self):
        if(self.BLOCK_DIR[1:] not in os.listdir()):
            os.mkdir(os.curdir + self.BLOCK_DIR)
            self.add_block()
            logging.info('Created Genesis block in ' + self.BLOCK_FILENAME)

    def save_cur_block(self):
        if os.path.isfile(self.BLOCK_FILENAME) :
            file_dict = json.load(open(self.BLOCK_FILENAME))
            self.blocks_frame = file_dict
            logging.info('Previous blocks is saved!')        

    def add_block(self, title='Genesis block', vote_for=''):
        block = self.block.copy()
        block['title'] = title
        block['vote_for'] = vote_for
        block['timestamp'] = time.time()
        block['index'] = self.blocks_frame['blocks_count']
        index = self.blocks_frame['blocks_count']
        if(index != 0):
            block['prev_hash'] = self.get_block_hash(self.blocks_frame['blocks'][index-1])

        self.blocks_frame['blocks'].append(block)
        self.blocks_frame['blocks_count'] = self.blocks_frame['blocks_count'] + 1

        with open(self.BLOCK_FILENAME, 'w') as file:
            json.dump(self.blocks_frame, file, indent=4, ensure_ascii=False)
            logging.info('Created block with index: ' + str(self.blocks_frame['blocks_count'] - 1))

    def get_block_hash(self, block):
        try:
            return hashlib.sha256(json.dumps(block).encode()).hexdigest()
        except Exception as e:
            logging.error(e)

    def check_blocks_integrity(self) -> []:
        is_block_integrated = {
        'index' : 0,
        'result' : 0 # 1 - OK, 0 - not okey
        }
        result = list()
        for index in range(1, self.blocks_frame['blocks_count']):
            is_block_integrated['index'] = index - 1
            is_block_integrated['result'] = self.blocks_frame['blocks'][index]['prev_hash'] == self.get_block_hash(self.blocks_frame['blocks'][index - 1]) # Красивая строка :)
            result.append(is_block_integrated.copy())
        return result



if __name__ == '__main__':
    b = BlockChain()
    b.creat_genesis_block()
    b.add_block("1", "1")
    b.add_block('2', "2")
    b.add_block('3', "3")
    print(b.check_blocks_integrity())
   

