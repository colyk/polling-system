import hashlib
import json
import os
import time
import logging

POLL_DIRNAME = 'polls'


class BlockChain():
    def __init__(self, poll_name='blocks', logdir='logs'):
        # TODO: logs must insist poll title.
        #Possibly use poll_name as a title
        if(logdir not in os.listdir()):
            os.mkdir(logdir)

        logging.basicConfig(filename=logdir + "/blockchain.log", level=logging.NOTSET,
                            format='%(levelname)s:%(asctime)s:%(message)s')

        self.BLOCK_DIR = POLL_DIRNAME
        self.BLOCK_FILENAME = '%s/%s/%s' % (os.curdir,
                                            POLL_DIRNAME, (lambda name: name if name.endswith('.json') else name+'.json')(poll_name))

        # Добавить id голосующего (Fingerprint) https://github.com/Valve/fingerprintjs
        self.block = {'title': '',
                      'vote_state': {},
                      'prev_hash': '',
                      'timestamp': '',
                      'index': 0
                    }

        self.blocks_frame = {
            'blocks': [],
            'blocks_count': 0
        }
        

    def init_check(self):
        if self.BLOCK_DIR not in os.listdir():
            os.mkdir(self.BLOCK_DIR)
            return 0
        elif not os.path.isfile(self.BLOCK_FILENAME):
            return 0
        else:
            try:
                return json.load(open(self.BLOCK_FILENAME))['blocks'][0]['title'][:2] == 'G_'
            except Exception:
                logging.error('File existed but no genesis block found')
                return 0


    def load_prev_blocks(self):
        file_dict = json.load(open(self.BLOCK_FILENAME))
        self.blocks_frame = file_dict
        logging.info('Loaded blocks from %s' % self.BLOCK_FILENAME)
    
    
    def create_block(self, init=False, title='NO_TITLE', vote_for=''):
        #init could be False or list of vote options
        block = self.block.copy()
        if (init):
            #Genesis block starts with 'G_'
            atitle = 'G_' + title
            #if init then create dictionary with vote options and zero vote counts
            opts = [(opt, 0) for opt in init]
            block['vote_state'].update(opts)
        else:
            lastblock = self.blocks_frame['blocks'][-1]
            #title = last title if last block's title starts not with "G_"
            atitle = (lambda s: lastblock['title'][2:] if s else lastblock['title'])(lastblock['title'][:2] == 'G_')
            #last vote state
            block['vote_state'] = lastblock['vote_state'].copy()
            #try to increase vote count by 1, if such option exists
            if vote_for in block['vote_state']:
                block['vote_state'][vote_for] += 1
        #common stuff
        block['title'] = atitle
        block['timestamp'] = time.time()
        
        return block

    def add_block(self, block):
        #actually add and write block
        index = self.blocks_frame['blocks_count']
        block['index'] = index
        if(index != 0):
            block['prev_hash'] = self.get_block_hash(
                self.blocks_frame['blocks'][index - 1])
        self.blocks_frame['blocks'].append(block)
        self.blocks_frame['blocks_count'] += 1

        with open(self.BLOCK_FILENAME, 'w') as file:
            try:
                json.dump(self.blocks_frame, file,
                          indent=4, ensure_ascii=False)
                logging.info('Created block with index: ' +
                             str(self.blocks_frame['blocks_count'] - 1))
                return b
            except Exception:
                logging.exception('An exception occured when tried to write block %s to %s' %
                                  (str(blocks_frame['blocks_count'] - 1), self.BLOCK_FILENAME))

    # Подумать о закрытии блоков кешем файла
    def get_block_hash(self, block):
        try:
            return hashlib.sha256(json.dumps(block).encode()).hexdigest()
        except Exception:
            logging.exception(
                'An exception occured when tried to get hash %s block' % str(block['index']))

    def check_blocks_integrity(self) -> []:
        result = list()
        is_block_integrated = {
            'index': 0,
            'result': 0
        }
        for index in range(1, self.blocks_frame['blocks_count']):
            is_block_integrated['index'] = index - 1
            is_block_integrated['result'] = self.blocks_frame['blocks'][index][
                'prev_hash'] == self.get_block_hash(self.blocks_frame['blocks'][index - 1])

            if not is_block_integrated['result']:
                logging.warning('Integrity check failed for block %s' %
                                is_block_integrated['index'])
            result.append(is_block_integrated.copy())
        if not result:
        	logging.warning("There are no blocks to check poll_name: %s" % self.poll_name)
        return result

    def get_current_blocks(self):
        return self.blocks_frame

    @property
    def blocks_count(self):
    	return self.blocks_frame['blocks_count']

    @property
    def blocks_filename(self):
    	return self.BLOCK_FILENAME


if __name__ == '__main__':
    '''
    just an example
    The idea is to use PollingSystem as wrapper for this with stuff like 

    def create_poll(title, options): 
        if not init_check():
            create_block(init=options, title=title)
        ...
    (because create_block with 'init' list creates genesis block)

    and something like

    def vote_for(option):
        new_block = BlockChain.create_block(vote_for=option)
        BlockChain.add_block(new_block)
        ...
    
    Also something like general json file and polls_frame that keeps all opened poll titles

    Then, implement this in api
    possibly with user id checks
    '''
    import random

    b = BlockChain(poll_name='Test_poll')
    new_init = b.create_block(init=['trumpet', 'violin', 'trombone'], title='Test')
    b.add_block(new_init)

    for i in range(10):
        new = b.create_block(vote_for=random.choice(['trumpet', 'violin', 'trombone', 'nothing']))
        b.add_block(new)

    print(b.check_blocks_integrity())
    print(b.blocks_filename)

