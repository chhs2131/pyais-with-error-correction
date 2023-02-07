from datetime import datetime

class AisLog:
    def __init__(self, log_message):
        self.ais, self.datetime = self.parser(log_message)

    def parser(self, log_message):
        tokens = log_message.split()
        print(tokens)
        if len(tokens) == 1:
            return tokens[0], None
        if len(tokens) != 3:
            raise
        return tokens[2], datetime.strptime(tokens[0] + " " + tokens[1], '%Y-%m-%d %H:%M:%S.%f')

    def getAis(self):
        return self.ais

    def getDatetime(self):
        return self.datetime


if __name__ == "__main__":
    example_messages = [
        "2023-02-07 00:36:09.765286 !AIVDM,1,1,,B,16Tp:4?000a3P@>EKu6efjd>0<65,0*0A",
        "",
        "2023-02-07 00:36:09.859035 !AIVDM,1,1,,B,16S`nr00h093JRTEEtM8UbN6086u,0*16",
        "!AIVDM,1,1,,B,16ShdKPP00a3SsPEKDwf4?vB2@5k,0*5C"
    ]

    for msg in example_messages:
        try:
            ais_log = AisLog(msg)
            print(ais_log.getAis(), ais_log.getDatetime())
        except:
            print("blank?: ", msg)
