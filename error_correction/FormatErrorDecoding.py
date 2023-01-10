from pyais import decode as ais_decode
from pyais import util
class FormatDecoder:
    def decode(self, raw_data):
        last_field = self.pick_last_field(raw_data)
        binary_raw_data = bytes(last_field, 'utf-8')

        return util.decode_into_bit_array(binary_raw_data)

    def decode_with_checksum(self, raw_data):
        # util.decode_into_bit_array()
        return raw_data

    def pick_last_field(self, raw_data):
        r = raw_data.split(',')
        return r[len(r) - 1].strip()
