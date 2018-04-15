import zipfile  # dafault installed in python v 3.5+
import os
import logging
import json
import hashlib

from blockchain import BlockChain
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

    @staticmethod
    def is_fake(result):
        return all(not element['result'] for element in result)

    @staticmethod
    def get_active_polls() -> {}:
        result = {
            'polls': []
        }
        if not os.path.exists(BLOCK_DIRNAME):
            return result
        for file in os.listdir(BLOCK_DIRNAME):
            try:
                result['polls'].append(
                    json.load(open(BLOCK_DIRNAME + "/" + file))['title'])
            except Exception:
                logger.warning(
                    "Poll in file %s is not valid, no title found" % file)
        return result

    def vote(self, vote_for):
        return self.add_block(vote_for)

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
        # Some block is corrupted
        if PollingSystem.is_fake(result):
            return 0
        # Any block is not corrupted
        else:
            return self.last_block['vote_state']

    def zip_poll(self):
        old_polls_arch = zipfile.ZipFile(ARCHIVE_PATH, 'a')
        old_polls_arch.write(self.BLOCK_FILENAME,
                             arcname=self.BLOCK_FILENAME.split('/')[-1])
        old_polls_arch.close()
        os.remove(self.BLOCK_FILENAME)

    @staticmethod
    def get_archived_polls(encrypted=False) -> []:
        archived_polls = list()
        myzip = zipfile.ZipFile(ARCHIVE_PATH, 'r')
        for poll in myzip.namelist():
            archived_polls.append(poll.split('/')[-1])

        if encrypted:
            return archived_polls
        else:
            return [json.loads(myzip.read(file).decode('utf-8'))['title'] for file in archived_polls]

    @staticmethod
    def get_zipped_info(filename):
        filename = hashlib.sha224(filename.encode()).hexdigest() + '.json'
        infos = list()
        info = {
            'title': '',
            'description': '',
            'voters': 0,
            'termination_time': '',
            'vote_state': {}
        }
        myzip = zipfile.ZipFile(ARCHIVE_PATH, 'r')

        for file in myzip.namelist():
            if file == filename:
                zipped_file = json.loads(myzip.read(file).decode('utf-8'))
                info['title'] = zipped_file['title']
                info['description'] = zipped_file['description']
                info['voters'] = zipped_file['blocks_count'] - 1
                info['termination_time'] = zipped_file['blocks'][0]['termination_time']
                info['vote_state'] = zipped_file['blocks'][-1]['vote_state']
                infos.append(info.copy())

        return infos


if __name__ == '__main__':

    p = PollingSystem.add_poll(options=['lol'], poll_name='blocks', termination_time=0, description='')
    # p.vote('lol')
    # p.vote('lol')
    # p.vote('lol')
    # p.vote('lol')
    # p.vote('lol')
    p.zip_poll()
    # p = PollingSystem.load_poll()
    # for i in range(100):
    # p = PollingSystem.load_poll('qqqq')
    # p.vote('ku')
    # print(p.get_poll_result(True))

    print(PollingSystem.get_archived_polls())
    # for i in PollingSystem.get_zipped_info('blocks'):
        # print(i)

    # print(p.get_info())
    # print(PollingSystem.get_active_polls())
    # p.zip_poll()
