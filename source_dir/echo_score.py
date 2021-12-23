import json

def init():
    print('this initializes the model')


def run(data):
    test = json.loads(data)
    print(f"received data: {test}")
    return f"test is {test}"