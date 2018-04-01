import hashlib
import json
import os
import time
import logging

POLL_DIRNAME = 'polls'


class BlockChain():

    def __init__(self, poll_filename='blocks.json', logdir='logs'):
        # TODO: logs must insist poll title.
        if(logdir not in os.listdir()):
            os.mkdir(logdir)

        logging.basicConfig(filename=logdir + "/blockchain.log", level=logging.NOTSET,
                            format='%(levelname)s:%(asctime)s:%(message)s')

        if(not poll_filename.endswith('.json')):
            poll_filename += '.json'

        self.BLOCK_DIR = POLL_DIRNAME
        self.BLOCK_FILENAME = '%s/%s/%s' % (os.curdir,
                                            POLL_DIRNAME, poll_filename)

        # Поле тайтл только у генезис блока.
        # Варианты голосования в генезиз блоке. Другой вариант блока для генезиз блока.
        # Добавить id голосующего (Fingerprint)
        # https://github.com/Valve/fingerprintjs
        self.block = {'vote_for': '',
                      'previous_hash': '',
                      'timestamp': '',
                      'index': 0
                      }

        self.blocks_frame = {
            'blocks': [],
            'blocks_count': 0,
            'options': [],
            'title': ''

        }

        # TODO: переделать, так как этот код исполняется при наследовании в
        # PollSystem
        if not self.init_check():
            self.create_genesis_block()
        else:
            self.load_prev_blocks()

        logging.info('Created BlockChain object in %s with poll_name %s' %
                     (POLL_DIRNAME, poll_filename))

    def init_check(self):
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

    def create_genesis_block(self):
        self.add_block()
        logging.info('Created Genesis block in %s' % self.BLOCK_FILENAME)

    def load_prev_blocks(self):
        file_dict = json.load(open(self.BLOCK_FILENAME))
        self.blocks_frame = file_dict
        logging.info('Loaded blocks from %s' % self.BLOCK_FILENAME)

    # Генезиз блок может иметь тайтл вида: Gen block. TITLE. Тогда можно исп.
    # split('.')
    def add_block(self, title='Genesis block', vote_for=''):
        block = self.block.copy()
        block['title'] = title
        block['vote_for'] = vote_for
        block['timestamp'] = time.time()
        block['index'] = self.blocks_frame['blocks_count']
        index = self.blocks_frame['blocks_count']
        if(index != 0):
            block['prev_hash'] = self.get_block_hash(
                self.blocks_frame['blocks'][index - 1])

        self.blocks_frame['blocks'].append(block)
        self.blocks_frame['blocks_count'] = self.blocks_frame[
            'blocks_count'] + 1

        with open(self.BLOCK_FILENAME, 'w') as file:
            try:
                json.dump(self.blocks_frame, file,
                          indent=4, ensure_ascii=False)
                logging.info('Created block with index: ' +
                             str(self.blocks_frame['blocks_count'] - 1))
            except Exception:
                logging.exception('An exception occured when tried to write block %s to %s' %
                                  (str(blocks_frame['blocks_count'] - 1), self.BLOCK_FILENAME))

    # Подумать о закрытии блоков кешем файла
    def get_block_hash(self, block) -> str:
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
            logging.warning(
                "There are not blocks to check poll_name: %s" % self.poll_name)
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
    b = BlockChain()
    b.add_block("1", "1")
    b.add_block('2', "1")
    b.add_block('2', "22")
    print(b.check_blocks_integrity())
    print(b.blocks_filename)
