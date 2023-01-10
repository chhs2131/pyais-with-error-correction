from pyais import decode as ais_decode

class NormalDecoder:
    def decode(self, raw_data):
        raw_data = self.strip(raw_data)
        return ais_decode(raw_data)

    def decode_without_checksum(self, raw_data):
        raw_data = self.strip(raw_data)
        raw_data += '0*00'  # 임의로 checksum 추가
        return ais_decode(raw_data)

    def strip(self, raw_data):
        return raw_data.strip()  # 개행 문자 오류 제거
