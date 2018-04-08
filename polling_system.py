from blockchain import BlockChain
import zipfile  # dafault installed in python v 3.5+
import os
import logging
import json

from config import *

logger = logging.getLogger(__name__)

logging.basicConfig(filename=LOG_PATH, level=logging.NOTSET,
                    format='%(name)s:%(levelname)s:%(asctime)s:%(message)s')


class PollingSystem(BlockChain):

    def __init__(self, options, termination_time=0, is_added=True, poll_name='blocks', description=''):
        super().__init__(description, poll_name)
        logger.info('Created PollingSystem object in %s with title %s' %
                    (BLOCK_DIRNAME, poll_name))
        self.poll_name = poll_name
        if is_added:
            self.create_genesis_block(options, termination_time)
        else:
            if self.is_path_exist():
                self.load_prev_blocks()
            else:
                logger.warning(
                    "Сan't load poll %s, because path doesn't exist" % poll_name)

    @classmethod
    def add_poll(cls, options, poll_name='blocks', termination_time=0, description=''):
        logger.info('Created PollingSystem object')
        return cls(options, termination_time, True, poll_name, description)

    @classmethod
    def load_poll(cls, poll_name='blocks'):
        logger.info('Loaded PollingSystem object')
        return cls(is_added=False, poll_name=poll_name, options=[])

    def vote(self, vote_for):
        return self.add_block(vote_for)

    @staticmethod
    def is_fake(result):
        for element in result:
            if not element['result']:
                return True
        return False

    @staticmethod
    def get_active_polls():
        result = {
            'polls': []
        }
        for file in os.listdir(BLOCK_DIRNAME):
            try:
                result['polls'].append(json.load(open(BLOCK_DIRNAME + "/" + file))['title'])
            except Exception as e:
                logger.warning(
                    "Poll in file %s is not valid, no title found" % file)
        return result

    def get_info(self):
        info = {
            'title': self.blocks_frame['title'],
            'description': self.blocks_frame['description'],
            'voters': self.blocks_count - 1,
            'termination_time': self.first_block['termination_time'],
            'vote_state': self.last_block['vote_state']
        }
        return info

    def get_poll_result(self, count_corrupted_blocks=False):
        result = self.check_blocks_integrity()

        if count_corrupted_blocks:
            return self.last_block['vote_state']

        if PollingSystem.is_fake(result):
            logger.info('Some block is corrupted.')
            return 0
        else:
            logger.info('Any block is not corrupted.')
            return self.last_block['vote_state']

    def zip_poll(self):
        # Закрытие последний блоком - хеш файла
        old_polls_arch = zipfile.ZipFile(ARCHIVE_PATH, 'w')
        old_polls_arch.write(self.BLOCK_FILENAME)
        old_polls_arch.close()
        os.remove(self.BLOCK_FILENAME)


    def load_from_zip(self):
        pass


if __name__ == '__main__':
    p = PollingSystem.add_poll(['bu', 'ku'], termination_time=0)
    p.vote('bu')
    # p.zip_poll()

    # p = PollingSystem.load_poll()
    # for i in range(100):
    # p.vote('ku')
    print(p.get_poll_result(False))
    print(p.get_info())
    print(PollingSystem.get_active_polls())
