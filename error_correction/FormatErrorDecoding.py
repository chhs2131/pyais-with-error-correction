from pyais import decode as ais_decode
from pyais import util
import re

CHECKSUM_PATTERN = '\d\*\d\d$'


class FormatDecoder:
    def decode(self, raw_data):
        last_field, fill_bit = self.pick_last_field(raw_data)
        binary_raw_data = bytes(last_field, 'utf-8')

        return util.decode_into_bit_array(binary_raw_data, fill_bit)

    def decode_with_checksum(self, raw_data):
        last_field, fill_bit = self.pick_last_field(raw_data)
        binary_raw_data = bytes(last_field, 'utf-8')

        return util.decode_into_bit_array(binary_raw_data, fill_bit)

    def pick_last_field(self, raw_data):
        # 체크섬이 존재하는 경우
        checksum_field = re.search(CHECKSUM_PATTERN, raw_data)
        fill_bit = 0
        if checksum_field is not None:
            fill_bit = int(checksum_field.group()[0])  # Fillbit를 확인
            raw_data = re.sub(CHECKSUM_PATTERN, '', raw_data)  # Checksum Field는 삭제
            raw_data.rstrip(',')

        # 마지막 필드를 가져온다
        r = raw_data.split(',')
        return r[len(r) - 1].strip(), fill_bit
