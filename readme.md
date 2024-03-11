# Алгоритмы разбора КС-грамматик
В данном репозитории представленна реализация алгоритмов Эрли и Кока-Янгера-Касами.

## Алгоритм Эрли

Реализация алгоритма Эрли разбора КС-грамматик.

#### Описание
Класс `EarlyParser` принимает на вход путь к `.txt` файлу с описанием грамматики
в формате **BNF**.  

* Метод `.parse()` экземпляра класса принимает на вход слово в формате последовательности элементов
алфавита грамматики, **каждый в двойных кавычках**, в python-списке. Возвращает `true`, если слово выводится в заданной грамматике и `false` иначе.  
`.parse()` реализует запрос, поэтому для экземпляра класса доступно произвольное
количество вызовов метода, все они отработают корректно.

* `.get_grammar()` возвращает строку-грамматику класса в формате BNF. 


#### Пример использования

```python

from early.parser import EarlyParser

parser = EarlyParser('tests/data/BNF_example.txt')

res = parser.parse(['"a"', '"b"'])  # equals to ab
```

#### Тестирование
Результаты тестов можно посмотреть через `github actions`, процент покрытия в
**отчете CI** в комментариях к последнему коммиту.

#### UML
![UML](early/EarlyUML.png)

## Алгоритм Кока-Янгера-Касами + приведение к нормальной форме Хомского (_НФХ_)

Реализация алгоритма Кока-Янгера-Касами разбора КС-грамматик для произвольной грамматики.

#### Описание
Класс `CYKParser` принимает на вход путь к `.txt` файлу с описанием грамматики
в формате **BNF** и флаг "_является грамматикой в НФХ_"  

* Метод `check_word` экземпляра класса принимает на вход слово в формате 
последовательности элементов алфавита грамматики, **каждый в двойных кавычках**, в python-списке. Возвращает `true`, если слово выводится в заданной грамматике и `false` иначе.  
`.parse()` реализует запрос, поэтому для экземпляра класса доступно произвольное
количество вызовов метода, все они отработают корректно.

* Класс `Converter` представляет из себя вспомогательный класс, который реализует
приведение к _НФХ_.
```python
from src.CYK.CYK import CYKParser

parser = CYKParser('BNF_example.txt', is_in_ch_nf=False)

res = parser.check_word(['"a"', '"b"'])  # equals to ab
```
#### Тестирование
Покрытие тестами - _91%_. Все, что не покрыто в `CYKParser` - считывание _BNF_ 
грамматики в _НФХ_. Этот код аналогичен коду из `Converter`, который **покрыт** 
тестами.

#### UML

![UML CYK + Converter to Chomsky normal form](src/CYK_and_Converter_UML.png)
