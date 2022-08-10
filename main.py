import json
from _datetime import datetime
import os

name_file = 'logs'
start = datetime.now()

open(os.path.join(f"{name_file}.txt"), "w", encoding='utf-8').close()
with open(os.path.join(f"{name_file}.txt"), "a", encoding='utf-8') as f:
    f.write(f'Starting code: {str(start)}, take it as 0\n')

nested_list = [
    ['a', 'b', 'c'],
    ['d', [['e', 'x']], [[['f']]], 'h', False],
    [1, [[2]], None, 'h'],
    ['e', 'f', ['h', 1]],
    ['5', ['6'], '9', [4, 6, 8], [7, 8]]
]


def logger(name_file, start):
    def create_log(func):
        def decor_func(*args, **kwargs):
            result = func(*args, **kwargs)
            log = f'Time: {str(datetime.now() - start)}, Name: {func.__name__}, args: {args}, kwargs: {kwargs}, result: {result}\n'
            with open(os.path.join(f"{name_file}.txt"), "a", encoding='utf-8') as file:
                file.write(log)
            return result
        return decor_func
    return create_log


class FlatIterator:
    @logger(name_file, start)
    def __init__(self, nested_list):
        result = self.unpacker(nested_list)
        self.start = result[0]
        self.end = len(result)

    @logger(name_file, start)
    def __iter__(self):
        self.cursor = -1
        return self

    @logger(name_file, start)
    def __next__(self):
        self.cursor += 1
        if self.cursor >= self.end:
            raise StopIteration
        return nested_list[self.cursor]

    @logger(name_file, start)
    def unpacker(self, nested_list):
        if type(nested_list) is list:
            list_checker = [1]
        while list_checker.count(1) > 0:
            result = []
            for i in nested_list:
                if type(i) is list:
                    for j in i:
                        result.append(j)
                    nested_list.remove(i)
            for i in result:
                nested_list.append(i)
            list_checker = []
            for i in nested_list:
                if type(i) is list:
                    list_checker.append(1)
                else:
                    list_checker.append(0)
        return nested_list


print(f'Вывод запроса: for item in FlatIterator(nested_list):')
for item in FlatIterator(nested_list):
    print(item)

print(f'\nВывод запроса: flat_list = [item for item in FlatIterator(nested_list)]')
flat_list = [item for item in FlatIterator(nested_list)]
print(flat_list)
