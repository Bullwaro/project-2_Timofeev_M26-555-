import prompt

def welcome():
    print("Первая попытка запустить проект!")
    print(
        """
        ***
        <command> exit - выйти из программы
        <command> help - справочная информация
        """
        )
    while True:
        
        command = prompt.string("Введите команду: ")
        match command:
            case "help":
                print(
                    """
                    <command> exit - выйти из программы
                    <command> help - справочная информация
                    """
                    )
            case "exit":
                print("База данных завершила свою работу")
                break