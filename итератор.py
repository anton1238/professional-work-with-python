class FlatIterator:
    def __init__(self, multi_list):
        self.multi_list = multi_list
    def __iter__(self):
        self.list_iter = iter(self.multi_list)
        self.nested_list = []
        self.cursor = -1
        return self
    def __next__(self):
        self.cursor += 1
        if len(self.nested_list) == self.cursor:
            self.nested_list = None
            self.cursor = 0
            while not self.nested_list:
                self.nested_list = next(self.list_iter)
def flat_generator(my_list):
    for sub_list in my_list:
        for elem in sub_list:
            yield elem
if __name__ == '__main__':
    nested_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None],
    ]
    print('*' * 20)
    for item in FlatIterator(nested_list):
        print(item)
    print('*' * 20)
    print('_' * 20)
    flat_list = [item for item in FlatIterator(nested_list)]
    print(flat_list)
    print('_' * 20)
    print('+' * 20)
    for item in flat_generator(nested_list):
        print(item)
    print('+' * 20)