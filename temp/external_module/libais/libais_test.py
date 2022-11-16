import ais.stream

with open("ais_20211104_15.txt") as f:
    n =  0
    for msg in ais.stream.decode(f):
        print(msg)
        # try:
        #     print(msg)
        # except Exception as e:
        #     print(e)
