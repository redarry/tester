## Описание
Эта программа преднозначена для быстрого тестирования задач на программирование. Для тестирования используются наборы тестов в формате *.json. 
## Инструкция по использованию
### Формат тестов
Как было сказано выше, тесты пишутся в формате *.json. Ключем в файле является название теста, а значением словарь с 2 ключами: "input" и "output", значениями которых соответственно являются входные и выходные данные.
Входные данные указываются в формате строки.
Выходные данные могут быть строкой, или списком строк. Если указана одна строка, то результат работы программы должен совпадать с указанной строкой. Если же указан список со строками, то тест будет засчитан если результат работы программы содержится в указанном списке.
Пример файла с тестами:
```json
{
  "test 1": {"input": "1", "output": "1"},
  "test 2": {"input": "2", "output": "2"},
  "test 3": {"input": "3", "output": ["4", "5"]}
}
```
### Типы тестов
Данная программа тестирования для запуска кода использует файлы с описанием команд для запуска определенного кода. Благодаря этому можно писать собственные типы тестов и тестировать код, написанный проктически на любом языке программирования.
Конфигурационный файл типа теста имеет всего 3 аргумента: **INIT_COMMAND**, **MAIN_COMMAND** и **FINAL_COMMAND**, в которых соответственно указываются команды для подготовки программы к исполнению, запуска программы и завершения работы с программой.
Вместо самого файла программы в таком файле стоит указывать [file], вместо которого позже автоматически будет подставлен тестируемый файл.
Пример конфигурационного файла типа теста для языка python:
```
[Commands]
INIT_COMMAND=
MAIN_COMMAND=python [file]
FINAL_COMMAND=
```
### Аргументы и опции
```
positional arguments:
  program               program for testing
  tests                 JSON file with tests

options:
  -h, --help            show this help message and exit
  --time TIME           maximum program execution time
  --type TYPE           type of program
  -i INPUT_FILE, --input-file INPUT_FILE
                        input file
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        output file
  --encoding ENCODING   encoding of input and output files
```
