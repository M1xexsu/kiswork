Задание №1
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу 
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. 
Эмулятор должен запускаться из реальной командной строки, а файл с 
виртуальной файловой системой не нужно распаковывать у пользователя. 
Эмулятор принимает образ виртуальной файловой системы в виде файла формата 
tar. Эмулятор должен работать в режиме CLI.
Ключами командной строки задаются:
• Имя пользователя для показа в приглашении к вводу.
• Имя компьютера для показа в приглашении к вводу.
• Путь к архиву виртуальной файловой системы.
• Путь к лог-файлу.
• Путь к стартовому скрипту.
Лог-файл имеет формат csv и содержит все действия во время последнего 
сеанса работы с эмулятором. Для каждого действия указаны дата и время. Для 
каждого действия указан пользователь.
Стартовый скрипт служит для начального выполнения заданного списка 
команд из файла.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также 
следующие команды:
1. du.
2. uname.
3. rmdir.
Все функции эмулятора должны быть покрыты тестами, а для каждой из 
поддерживаемых команд необходимо написать 2 теста.