from blockchain import BlockChain


class PollingSystem(BlockChain):

    def __init__(self):
        super().__init__()

    # Создание файла
    @classmethod
    def add_poll(cls, title, vote_for):
        pass
    
    # Добавление блока
    def vote(self, poll_name):
    	pass

    # hashmap with % ({'Barak':23.2, "Bush":76.8})
    def get_poll_result(self):
        pass

    # Удаление блока голосования (Файла), после получения результата
    def __del__(self):
        pass

    # Вывод информации о голосании: Кандидаты, кол. гол.
    def __str__(self):
        return ''


if __name__ == '__main__':
	p = PollingSystem()