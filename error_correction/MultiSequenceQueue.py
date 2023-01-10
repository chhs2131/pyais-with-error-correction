from pyais import decode


class MultiSequenceQueue:
    def __init__(self):
        self.queue = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [], "9": []}

    '''
    list에 멀티메세지를 추가
    2개가 모일 경우에 둘을 합친 list를 반환함 
    '''

    def decode(self, message):
        message_list = self.addMessage(message)
        return self.decodeList(message_list)

    def addMessage(self, message):
        self.validateMultiSequenceMsg(message)

        msg = message.split(',')
        target = msg[3]
        self.queue[target].append(message)
        if len(self.queue[target]) == 2:
            result = self.queue[target]
            self.queue[target] = []
            return result

    def validateMultiSequenceMsg(self, message):
        msg = message.split(',')
        if msg[1] == 1 or msg[1] == "1":
            raise ValueError("싱글 시퀀스 메세지입니다.")

    def decodeList(self, message_list):
        if message_list is not None:
            return decode(*message_list)

    def checkSequenceQueue(self):
        pass

    def isSequenceComplete(self):
        pass

    def listCompleteMultiMessage(self):
        pass

    def decodeMultiMessage(self):
        pass


if __name__ == '__main__':
    multiSequenceQueue = MultiSequenceQueue()

    # RAW DATA 파일 불러오기
    file_path = './data/ais_20211104_15.txt'

    with open(file_path) as f:
        lines = f.readlines()
        for msg in lines:
            data = msg
            try:
                result = multiSequenceQueue.decode(data)
                if result is not None:
                    print(result.to_json())
            except Exception as e:
                print(e, data)
                # pass
