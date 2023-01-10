from pyais import IterMessages

if __name__ == '__main__':
    # RAW DATA 파일 불러오기
    file_path = './ais_20211104_15.txt'

    with open(file_path) as f:
        lines = f.readlines()

        result = []
        for line in lines:
            result.append(bytes(line, 'utf-8'))

        lines = result
        try:
            for msg in IterMessages(lines):
                print('ori', msg)
                print(msg.decode())
        except Exception as e:
            print('exception' + str(e))
