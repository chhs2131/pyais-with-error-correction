# !AIVDM,1,1,,A,16Sd0KUq1o93PMbEG=T3Pi>L0<7E,0*0F
# 포맷을 확인하여 각 로직으로 전달하는 역할
# 정상 메세지 -> 디코딩 로직
# 멀티 메세지 -> 멀티메세지 큐 -> 디코딩 로직
# 포맷이상 메세지 -> Payload 추출 -> 전용 decode 로직 -> 추가로 검증도 필요
import datetime
import time
import traceback
import re

from pyais.exceptions import UnknownMessageException

from type import NmeaFormatType
from type import AisLog
import NormalDecoding
import MultiSequenceQueue
import FormatErrorDecoding
from util.SerializeUtil import to_json_from
from util.SerializeUtil import to_dict_from_attr

import logging
logger = logging.getLogger()
handler = logging.FileHandler('decoding_dict.txt')
logger.addHandler(handler)


class NvmeCheck:
    nmea_type = NmeaFormatType.NmeaType
    normal_decoder = NormalDecoding.NormalDecoder()
    multi_decoder = MultiSequenceQueue.MultiSequenceQueue()
    format_decoder = FormatErrorDecoding.FormatDecoder()

    def chooseNmeaClass(self, raw_data):
        count = raw_data.count(',')
        if count <= 4:
            return self.nmea_type.TOO_SHORT  # 복구 불가능한 케이스
        if count != 6:
            return self.nmea_type.E_FORMAT

        nmea = raw_data.split(',')
        if nmea[1] != '1':
            return self.nmea_type.MULTI

        if self.isHaveChecksum(raw_data):
            return self.nmea_type.NORMAL  # 정상메세지
        return self.nmea_type.WITHOUT_CHECKSUM

    def isHaveChecksum(self, raw_data):
        return re.search('\d\*\d\d$', raw_data)

    def decodeNmeaMsg(self, nmeaClass, raw_data):
        if nmeaClass == self.nmea_type.NORMAL:
            return self.normal_decoder.decode(raw_data)
        if nmeaClass == self.nmea_type.WITHOUT_CHECKSUM:
            return self.normal_decoder.decode_without_checksum(raw_data)
        if nmeaClass == self.nmea_type.MULTI:
            return self.multi_decoder.decode(raw_data)
        if nmeaClass == self.nmea_type.E_FORMAT:
            return self.format_decoder.decode(raw_data)
        if nmeaClass == self.nmea_type.TOO_SHORT:
            pass


def printException(title, raw_data, body=""):
    if False:
        print("==========================================================")
        print('[' + title + ' Exception]', "\n",
              str(e), "\n  =>RAW:", raw_data, "\n",
              body)
        traceback.print_exc()
        time.sleep(1)
        print("==========================================================")
        print(flush=True)


if __name__ == '__main__':
    nvmeCheck = NvmeCheck()

    # RAW DATA 파일 불러오기
    # file_path = './data/ais_20211104_15.txt'
    file_path = './data/' + 'for_test'

    with open(file_path) as f:
        lines = f.readlines()
        for msg in lines:
            try:
                ais_msg, ais_datetime = AisLog.AisLog(msg).getAisAndDatetime()
            except Exception as e:
                continue

            try:
                nmeaClass = nvmeCheck.chooseNmeaClass(ais_msg)
                decoding_msg = nvmeCheck.decodeNmeaMsg(nmeaClass, ais_msg)
                if decoding_msg is None:
                    continue

                decoding_msg = to_dict_from_attr(decoding_msg)
                decoding_msg["datetime"] = ais_datetime
                logger.error(decoding_msg)
            except UnknownMessageException as e:
                printException(nmeaClass.name, ais_msg, "존재하지않는 MessageType입니다.")
            except Exception as e:
                printException(nmeaClass.name, ais_msg)
