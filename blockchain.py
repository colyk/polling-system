import hashlib
import json
import os
import time
import logging

POLL_DIRNAME = 'polls'
LOG_PATH = 'logs/blockchain.log'

logger = logging.getLogger(__name__)

logging.basicConfig(filename=LOG_PATH, level=logging.NOTSET,
                    format='%(name)s:%(levelname)s:%(asctime)s:%(message)s')


class BlockChain():

    def __init__(self, poll_name='blocks'):

        self.BLOCK_DIR = POLL_DIRNAME
        self.BLOCK_FILENAME = '%s/%s/%s' % (os.curdir,
                                            POLL_DIRNAME, (lambda name: name if name.endswith('.json') else name + '.json')(poll_name))

        # Добавить id голосующего (Fingerprint)
        # https://github.com/Valve/fingerprintjs
        self.block = {'vote_state': {},
                      'prev_hash': '',
                      'timestamp': '',
                      'index': 0,
                      'id': 0
                      }

        self.blocks_frame = {
            'blocks': [],
            'blocks_count': 0,
            'title': poll_name
        }
        
        logging.info('Created BlockChain object in %s with poll_name %s' %
                     (POLL_DIRNAME, poll_name))

    def init_check(self):
        if self.BLOCK_DIR not in os.listdir():
            os.mkdir(self.BLOCK_DIR)
            return 0
        elif not os.path.isfile(self.BLOCK_FILENAME):
            return 0
        else:
            try:
                return json.load(open(self.BLOCK_FILENAME))['blocks'][0]['prev_hash'] == 'Genesis_block'
            except Exception:
                logger.error('File existed but no genesis block found')
                return 0

    def load_prev_blocks(self):
        file_dict = json.load(open(self.BLOCK_FILENAME))
        self.blocks_frame = file_dict
        logger.info('Loaded blocks from %s' % self.BLOCK_FILENAME)

    def create_block(self, options):
        self.block['vote_state'].update(list(zip(options, '0' * len(options))))

    def handle_options(self, vote_for=''):
        block['vote_state'] = lastblock['vote_state'].copy()
        # try to increase vote count by 1, if such option exists
        if vote_for in block['vote_state']:
            block['vote_state'][vote_for] += 1

    def add_block(self, block):
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
                logger.info('Created block with index: ' +
                            str(self.blocks_frame['blocks_count'] - 1))
                return block
            except Exception:
                logger.exception('An exception occured when tried to write block %s to %s' %
                                 (str(blocks_frame['blocks_count'] - 1), self.BLOCK_FILENAME))

    # Подумать о закрытии блоков кешем файла
    @staticmethod
    def get_block_hash(block):
        try:
            return hashlib.sha256(json.dumps(block).encode()).hexdigest()
        except Exception:
            logger.exception(
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
                'prev_hash'] == BlockChain.get_block_hash(self.blocks_frame['blocks'][index - 1])

            if not is_block_integrated['result']:
                logger.warning('Integrity check failed for block %s' %
                               is_block_integrated['index'])
            result.append(is_block_integrated.copy())
        if not result:
            logger.warning(
                "There are no blocks to check poll_name: %s" % self.poll_name)
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
            BlockChain.create_block(init=options, title=title)
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
    new_init = b.create_block(['trumpet', 'violin', 'trombone'])
    b.add_block(new_init)

    for i in range(10):
        new = b.create_block(vote_for=random.choice(
            ['trumpet', 'violin', 'trombone', 'nothing']))
        b.add_block(new)

    print(b.check_blocks_integrity())
    print(b.blocks_filename)
