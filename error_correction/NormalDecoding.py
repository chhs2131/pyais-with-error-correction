from pyais import decode as ais_decode

class NormalDecoder:
    def decode(self, raw_data):
        raw_data = raw_data.rstrip('\n')  # 개행 문자 오류 제거
        return ais_decode(raw_data)

    def decode_without_checksum(self, raw_data):
        pass
