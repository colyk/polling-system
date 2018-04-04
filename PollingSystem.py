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
            super().create_genesis_block(options)
        else:
            if super().is_path_exist():
                super().load_prev_blocks()
            else:
                logger.warning(
                    "Сan't load poll %s, because path doesn't exist" % poll_name)

    @classmethod
    def add_poll(cls, is_added=True, poll_name='blocks', options=['lol', 'kek']):
        logger.info('Created PollingSystem object')
        return cls(poll_name=poll_name, options=options)

    @classmethod
    def load_poll(cls, poll_name='blocks'):
        logger.info('Loaded PollingSystem object')
        return cls(is_added=False, poll_name=poll_name)

    def vote(self, vote_for):
        super().add_block(vote_for)

    def get_poll_result(self, count_corrupted_blocks=False):
        result = super().check_blocks_integrity()
        if count_corrupted_blocks:
            return super().last_block['vote_state']

        if all(result):
            logger.info('Any block is not corrupted.')
            return super().last_block['vote_state']
        else:
            logger.info('Some block is corrupted.')

    def load_from_zip(self):
        pass

    def zip_poll(self):
        old_polls_arch = zipfile.ZipFile(ARCHIVE_PATH, 'w')
        old_polls_arch.write(super().blocks_filename)
        old_polls_arch.close()
        os.remove(super().blocks_filename)

    def __str__(self):
        return 'Amount of voters: %s; Title: %s; ' % (super().blocks_count, self.poll_name)


if __name__ == '__main__':
    # p = PollingSystem.add_poll()
    # p.vote('lol')
    # print(p)
    p = PollingSystem.load_poll()
    p.vote('kek')
    print(p.get_poll_result(True))
