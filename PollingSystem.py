from blockchain import BlockChain
import zipfile  # dafault installed in python v 3.5+
import os

ARCHIVE_PATH = os.curdir + '/old_polls.zip'  # Saving old (deleted) polls
LOG_PATH = 'logs/blockchain.log'

logger = logging.getLogger(__name__)

logging.basicConfig(filename=LOG_PATH, level=logging.NOTSET,
                    format='%(name)s:%(levelname)s:%(asctime)s:%(message)s')

class PollingSystem(BlockChain):
    """ 
        poll_dirname - стандартный, в 1 папке хранятся все голосования.
        poll_name - Название голосования. Каждое голосование имеет свой файл.
    """
    
    def __init__(self, poll_name='blocks', logdir='logs'):
        super().__init__(poll_name, logdir)
        self.poll_name = poll_name.split('.')[0]
        self.load_poll()

    # Создание файла
    def add_poll(self, options):
        super().create_genesis_block()
        super().create_block(self, options)

    def vote(self, title, vote_for):
        super().add_block(title, vote_for)

    def load_poll(self):
        if not super().init_check():
            self.create_genesis_block()
        else:
            self.load_prev_blocks()

        logging.info('Created BlockChain object in %s with poll_name %s' %
                     (POLL_DIRNAME, poll_filename))

    # hashmap with % ({'Barak':23.2, "Bush":76.8})
    def get_poll_result(self):
        pass

    # Удаление блока голосования (Файла), после получения результата
    def __del__(self):
        old_polls_arch = zipfile.ZipFile(ARCHIVE_PATH, 'w')
        old_polls_arch.write(super().blocks_filename)
        old_polls_arch.close()
        os.remove(super().blocks_filename)

    # Вывод информации о голосании: Кандидаты, кол. гол.
    def __str__(self):
        return 'Amount of voters: %s; Title: %s; ' % (super().blocks_count, poll_name.split('.')[0])


if __name__ == '__main__':
    p = PollingSystem()
    print(ARCHIVE_PATH)
