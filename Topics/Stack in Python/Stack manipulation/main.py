from collections import deque

q = deque()

n = int(input())

for i in range(n):
    do = input()
    operation = do.split(" ")[0]
    if operation == 'PUSH':
        element = do.split(" ")[1]
        q.append(element)
    elif operation == 'POP':
        q.pop()

for i in range(len(q)):
    print(q.pop())
