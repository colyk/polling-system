import hashlib
import json
import os
import time
import logging

from config import *


logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_PATH, level=logging.NOTSET,
                    format='%(name)s:%(levelname)s:%(asctime)s:%(message)s')


class BlockChain():

    def __init__(self, description='v', block_name='blocks'):
        if BLOCK_DIRNAME not in os.listdir():
            os.mkdir(BLOCK_DIRNAME)

        self.BLOCK_FILENAME = '%s/%s/%s' % (os.curdir,
                                            BLOCK_DIRNAME, hashlib.md5(block_name.encode()).hexdigest() + '.json')

        # TODO: Add voter's id (Fingerprint)
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
            'title': block_name,
            'description': description
        }

        logging.info('Created BlockChain object in %s with block_name %s' %
                     (BLOCK_DIRNAME, block_name))

    def is_path_exist(self):
        if not os.path.isfile(self.BLOCK_FILENAME):
            return 0
        else:
            try:
                return json.load(open(self.BLOCK_FILENAME))['blocks'][0]['prev_hash'] == 'Genesis block'
            except Exception:
                logging.error('File existed but without genesis block')
        return 0

    def create_vote_states(self, options):
        opts = [(opt, 0) for opt in options]
        self.block['vote_state'].update(opts)

    def load_prev_blocks(self):
        file_dict = json.load(open(self.BLOCK_FILENAME))
        self.blocks_frame = file_dict
        logging.info('Loaded blocks from %s' % self.BLOCK_FILENAME)

    def handle_options(self, vote_for) -> {}:
        next_vote_state = self.last_block['vote_state'].copy()
        if vote_for in self.last_block['vote_state']:
            next_vote_state[vote_for] = int(next_vote_state[vote_for]) + 1
        else:
            return 0
        return next_vote_state

    def create_genesis_block(self, options, termination_time):
        self.create_vote_states(options)

        block = self.block.copy()
        block['timestamp'] = time.time()
        block['index'] = 0
        block['termination_time'] = termination_time
        block['prev_hash'] = 'Genesis block'
        self.blocks_frame['blocks'].append(block)
        self.blocks_frame['blocks_count'] = 1
        self.write_block()

    def add_block(self, vote_for=''):
        block = self.block.copy()
        next_vote_state = self.handle_options(vote_for)
        if next_vote_state:
            block['vote_state'] = next_vote_state
        else:
            logging.warning('Invalid vote_for: %s' % vote_for)
            return 0
        block['timestamp'] = time.time()
        block['index'] = self.blocks_frame['blocks_count']
        block['prev_hash'] = BlockChain.get_block_hash(
            self.last_block)

        self.blocks_frame['blocks'].append(block)
        self.blocks_frame['blocks_count'] += 1
        self.write_block()
        return 1

    def write_block(self):
        with open(self.BLOCK_FILENAME, 'w') as file:
            try:
                json.dump(self.blocks_frame, file,
                          indent=4, ensure_ascii=False)
                logging.info('Created block with index: ' +
                             str(self.blocks_count))
            except Exception:
                logging.exception('An exception occured when tried to write block %s to %s' %
                                  (str(self.blocks_count), self.BLOCK_FILENAME))

    @staticmethod
    def get_block_hash(block):
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
        for index in range(1, self.blocks_count):
            is_block_integrated['index'] = index - 1
            is_block_integrated['result'] = self.blocks_frame['blocks'][index][
                'prev_hash'] == BlockChain.get_block_hash(self.blocks_frame['blocks'][index - 1])
            if not is_block_integrated['result']:
                logging.warning('Integrity check failed for block %s' %
                                is_block_integrated['index'])
            result.append(is_block_integrated.copy())
        return result

    @property
    def blocks_count(self):
        return self.blocks_frame['blocks_count']

    @property
    def last_block(self):
        return self.blocks_frame['blocks'][-1]

    @property
    def first_block(self):
        return self.blocks_frame['blocks'][0]


if __name__ == '__main__':
    b = BlockChain()
    # b.create_genesis_block(['a'], 0)
    b.load_prev_blocks()
    # b.add_block('a')
    # b.add_block('a')
    b.add_block('a')
    print(b.check_blocks_integrity())
    # b.load_prev_blocks()
