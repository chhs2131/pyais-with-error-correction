# !AIVDM,1,1,,A,16Sd0KUq1o93PMbEG=T3Pi>L0<7E,0*0F
# 포맷을 확인하여 각 로직으로 전달하는 역할
# 정상 메세지 -> 디코딩 로직
# 멀티 메세지 -> 멀티메세지 큐 -> 디코딩 로직
# 포맷이상 메세지 -> Payload 추출 -> 전용 decode 로직 -> 추가로 검증도 필요

import traceback
import re
from type import NmeaFormatType
import NormalDecoding
import MultiSequenceQueue
import FormatErrorDecoding


class NvmeCheck:
    nmea_type = NmeaFormatType.NmeaType
    normal_decoder = NormalDecoding.NormalDecoder()
    multi_decoder = MultiSequenceQueue.MultiSequenceQueue()
    format_decoder = FormatErrorDecoding.FormatDecoder()

    def chooseNmeaClass(self, raw_data):
        count = raw_data.count(',')
        if raw_data.count(',') != 6:
            # 마지막 4글자가 0*00 형태일 경우
            if self.isHaveChecksum(raw_data):  # 끝에 4글자 또는 쉼표포함 5글자를 제거한 후에 가장 뒤에있는 BLOCK을 가져오면 Payload만 가져오는 것이 된다.
                return self.nmea_type.E_FORMAT_WITH_CHECKSUM
            if count <= 4:
                return self.nmea_type.TOO_SHORT  # 복구 불가능한 케이스
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
        if nmeaClass == self.nmea_type.E_FORMAT_WITH_CHECKSUM:
            return self.format_decoder.decode_with_checksum(raw_data)
        if nmeaClass == self.nmea_type.E_FORMAT:
            return self.format_decoder.decode(raw_data)
        if nmeaClass == self.nmea_type.TOO_SHORT:
            pass


if __name__ == '__main__':
    nvmeCheck = NvmeCheck()

    # RAW DATA 파일 불러오기
    file_path = './data/ais_20211104_15.txt'

    with open(file_path) as f:
        lines = f.readlines()
        for msg in lines:
            data = msg
            nmeaClass = nvmeCheck.chooseNmeaClass(data)

            try:
                nvmeCheck.decodeNmeaMsg(nmeaClass, data)
            except Exception as e:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", '[' + nmeaClass.name + ']', str(e), data, flush=True)
                # traceback.print_exc()
