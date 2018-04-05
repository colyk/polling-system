from blockchain import BlockChain
import zipfile  # dafault installed in python v 3.5+
import os
import logging

from config import *

logger = logging.getLogger(__name__)

logging.basicConfig(filename=LOG_PATH, level=logging.NOTSET,
                    format='%(name)s:%(levelname)s:%(asctime)s:%(message)s')


class PollingSystem(BlockChain):

    def __init__(self, options, is_added=True, poll_name='blocks'):
        super().__init__(poll_name)
        logger.info('Created PollingSystem object in %s with title %s' %
                    (BLOCK_DIRNAME, poll_name))
        self.poll_name = poll_name
        if is_added:
            self.create_genesis_block(options)
        else:
            if self.is_path_exist():
                self.load_prev_blocks()
            else:
                logger.warning(
                    "Сan't load poll %s, because path doesn't exist" % poll_name)

    @classmethod
    def add_poll(cls, options, is_added=True, poll_name='blocks'):
        logger.info('Created PollingSystem object')
        return cls(poll_name=poll_name, options=options)

    @classmethod
    def load_poll(cls, poll_name='blocks'):
        logger.info('Loaded PollingSystem object')
        return cls(is_added=False, poll_name=poll_name, options=[])

    def vote(self, vote_for):
        return self.add_block(vote_for)

    def is_fake(self, result):
        for element in result:
            if not element['result']:
                return True
        return False

    def get_poll_result(self, count_corrupted_blocks=False):
        result = self.check_blocks_integrity()
        if count_corrupted_blocks:
            return self.last_block['vote_state']

        if self.is_fake(result):
            logger.info('Some block is corrupted.')
            return 0
        else:
            logger.info('Any block is not corrupted.')
            return self.last_block['vote_state']

    def load_from_zip(self):
        pass

    def zip_poll(self):
        old_polls_arch = zipfile.ZipFile(ARCHIVE_PATH, 'w')
        old_polls_arch.write(self.BLOCK_FILENAME)
        old_polls_arch.close()
        os.remove(self.BLOCK_FILENAME)

    def __str__(self):
        return 'Amount of voters: %s; Title: %s; ' % (self.blocks_count, self.poll_name)


if __name__ == '__main__':
    # p = PollingSystem.add_poll(['bu','ku'])
    # p.vote('bu')
    # print(p)
    # p.zip_poll()

    p = PollingSystem.load_poll('new')
    # print(p.vote(''))
    print(p.get_poll_result(False))
