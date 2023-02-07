import datetime

TEST_MSG = "2022-12-31 19:19:19.191919 !AIVDM,1,1,,A,16Tp:4?000a3P=VEKsQ@02jJ00S3,0*43"
msg = TEST_MSG.split()
dt = datetime.datetime.strptime(msg[0] + " " + msg[1], '%Y-%m-%d %H:%M:%S.%f')
ais = msg[2]
print(msg, dt, ais)
