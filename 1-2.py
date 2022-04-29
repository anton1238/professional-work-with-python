ballanced_dict = {
    '(': ')',
    '[': ']',
    '{': '}'
}

ballanced = [
    '(((([{}]))))',
    '[([])((([[[]]])))]{()}',
    '{{[()]}}'
]
unballanced = [
    '}{}',
    '{{[(])]}}',
    '[[{())}]'
]

class Stack(list):
    def isEmpty(self):
        return len(self) == 0
    def push(self, _item):
        self.append(_item)
    def pop(self):
        if not self.isEmpty():
            _item = self[-1]
            self.__delitem__(-1)
        return _item
    def peek(self):
        if not self.isEmpty():
            return self[-1]
    def size(self):
        return len(self)
def check_ballance(seq_):
    stack = Stack()
    for item_ in seq_:
        if item_ in ballanced_dict:
            stack.push(item_)
        elif item_ == ballanced_dict.get(stack.peek()):
            stack.pop()
        else:
            return False
    return stack.isEmpty()

if __name__ == '__main__':
    for seq in ballanced + unballanced:
        print(f'{seq:<30}{check_ballance(seq)}')