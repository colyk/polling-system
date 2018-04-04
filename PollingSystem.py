from blockchain import BlockChain
import zipfile  # dafault installed in python v 3.5+
import os
import logging

from config import *

logger = logging.getLogger(__name__)

logging.basicConfig(filename=LOG_PATH, level=logging.NOTSET,
                    format='%(name)s:%(levelname)s:%(asctime)s:%(message)s')


class PollingSystem(BlockChain):

    def __init__(self, is_added=True, poll_name='blocks', options=[]):
        super().__init__(poll_name)
        logger.info('Created PollingSystem object in %s with title %s' %
                    (BLOCK_DIRNAME, poll_name))
        self.poll_name = poll_name
        if is_added:
            super().create_genesis_block
        else:
            if super().is_path_exist():
                super().load_prev_blocks
            else:
                logger.warning(
                    "Çan't load poll %s, because path doesn't exist" % poll_name)

    @classmethod
    def add_poll(cls, poll_name='blocks', options=['lol', 'kek']):
        logger.info('Created PollingSystem object')
        return cls(poll_name=poll_name, options=options)

    @classmethod
    def load_poll(cls, poll_name='blocks'):
        logger.info('Loaded PollingSystem object')
        return cls(is_added=False, poll_name=poll_name)

    def vote(self, vote_for):
        super().add_block(vote_for)

    def get_poll_result(self):
        if all(super().check_blocks_integrity()):
            print("Blocks are OK")

    # def __del__(self):
    #     old_polls_arch = zipfile.ZipFile(ARCHIVE_PATH, 'w')
    #     old_polls_arch.write(super().blocks_filename)
    #     old_polls_arch.close()
    #     os.remove(super().blocks_filename)

    # Вывод информации о голосании: Кандидаты, кол. гол.
    # def __str__(self):
    # return 'Amount of voters: %s; Title: %s; ' % (super().blocks_count,
    # poll_name.split('.')[0])


if __name__ == '__main__':
    p = PollingSystem()