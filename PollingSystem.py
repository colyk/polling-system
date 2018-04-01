from blockchain import BlockChain
import zipfile  # dafault installed in python v 3.5+
import os

ARCHIVE_PATH = os.curdir + '/old_polls.zip'  # Saving old (deleted) polls


class PollingSystem(BlockChain):
    """ 
        poll_dirname - стандартный, в 1 папке хранятся все голосования.
        poll_name - Название голосования. Каждое голосование имеет свой файл.
    """
# Рaзделить логирование по __name__

    def __init__(self, poll_name='blocks.json', logdir='logs'):
        super().__init__(poll_name, logdir)
        self.poll_name = poll_name.split('.')[0]

    # Создание файла
    def add_poll(self):
        super().create_genesis_block()

    # Добавление блока
    # Тут как раз и видно что тайтл только в генезиз блоке
    def vote(self, title, vote_for):
        super().add_block(title, vote_for)

    def check_vote(self, vote_for):
        # Есть воут_фор в кандидатах
        pass


    def load_poll(self):
        pass

        """
        Этот код перенести с блокчейна сюда.
        if not super().init_check():
            super().create_genesis_block()
        else:
            super().load_prev_blocks()
        """

    # hashmap with % ({'Barak':23.2, "Bush":76.8})
    def get_poll_result(self):
        pass

    # Удаление блока голосования (Файла), после получения результата
    def __del__(self):
        old_polls_arch = zipfile.ZipFile(ARCHIVE_PATH, 'w')
        old_polls_arch.write(open(super().blocks_filename))
        old_polls_arch.close()
        os.remove(super().blocks_filename)

    # Вывод информации о голосании: Кандидаты, кол. гол.
    def __str__(self):
        print(dir(super()))
        return 'Amount of voters: %s; Title: %s; ' % (super().blocks_count, poll_name.split('.')[0])


if __name__ == '__main__':
    p = PollingSystem()
    print(ARCHIVE_PATH)
