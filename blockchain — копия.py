import hashlib
import json
import os
import time
import logging


class BlockChain():

    def __init__(self, poll_dirname='blocks', poll_filename='blocks.json', logdir='logs'):
        # TODO: logs must insist poll title.
        if(logdir not in os.listdir()):
            os.mkdir(logdir)

        logging.basicConfig(filename=logdir+"/blockchain.log", level=logging.NOTSET,
                            format='%(levelname)s:%(asctime)s:%(message)s')
        
        if(not poll_filename.endswith('.json')):
            poll_filename += '.json'
    
        self.BLOCK_DIR = poll_dirname
        self.BLOCK_FILENAME = '%s/%s/%s' % (os.curdir, poll_dirname, poll_filename)
    
        # TODO: add proof of work
        self.block = {'title' : '',
            'vote_for' : '',
            'prev_hash' : '',
            'timestamp' : '',
            'index' : 0
            }

        self.blocks_frame = {
            'blocks' : [],
            'blocks_count' : 0
        }

        if not self.init_check():
            self.creat_genesis_block()
        
        self.load_prev_block()

        logging.info('Created object with poll_dirname: ' + poll_dirname +'; poll_filename: ' + poll_filename)
        

    def init_check(self):
        #also need to check if genesis-block exists
        if self.BLOCK_DIR not in os.listdir():
            os.mkdir(self.BLOCK_DIR)
            return 0
        elif not os.path.isfile(self.BLOCK_FILENAME):
            return 0
        else:
            try:
                return json.load(open(self.BLOCK_FILENAME))['blocks'][0]['title'] == 'Genesis block'
            except Exception:
                logging.error('File existed but without genesis block')
                return 0
            
        
    def creat_genesis_block(self):
        self.add_block()
        logging.info('Created Genesis block in %s' % self.BLOCK_FILENAME)

    def load_prev_block(self):
        if os.path.isfile(self.BLOCK_FILENAME) :
            file_dict = json.load(open(self.BLOCK_FILENAME))
            self.blocks_frame = file_dict
            logging.info('Loaded blocks from %s' % self.BLOCK_FILENAME)   

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
            'result' : 0 # 1 - OK, 0 - not okay
        }
        result = list()
        for index in range(1, self.blocks_frame['blocks_count']):
            is_block_integrated['index'] = index - 1
            is_block_integrated['result'] = self.blocks_frame['blocks'][index]['prev_hash'] == self.get_block_hash(self.blocks_frame['blocks'][index - 1]) # Красивая строка :)
            result.append(is_block_integrated.copy())
        return result



if __name__ == '__main__':
    b = BlockChain()
    # b.add_block("1", "1")
    # b.add_block('2', "1")
    # b.add_block('2', "22")
    # b.add_block('3', "56")
    # b.add_block('3', "57")
    # print(b.check_blocks_integrity())
   

