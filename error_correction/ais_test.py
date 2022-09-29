from pyais import decode
from json import dumps, loads
import sys
import traceback

from collections import defaultdict
error_list = []  # Save Parsing Error Datas
error_count = defaultdict(int)


def list_to_file(write_file_path, var_list):
    with open(write_file_path, 'w') as lf:

        for vd in var_list:
            lf.write(vd)


def decode_ais_file(file):
    with open(file) as f:
            lines = f.readlines()
            for msg in lines:
                data = msg
                try:
                    ais_data = decode(data).to_json()
                    # print(decode(data))
                except Exception as e:
                    print(e, data)
                    if str(e) == "A NMEA message needs to have exactly 7 comma separated entries.":  # 특정 예외만 처리
                        error_list.append(data)
                    # traceback.print_exc()
                    error_count[str(e)] += 1
                    # print(f'[ERROR] Value {data} not in JSON/AIS format')


if __name__ == '__main__':
    # RAW DATA 파일 불러오기
    if len(sys.argv) <= 1:
        print("Insufficient arguments")
        sys.exit()
    file_path = sys.argv[1]

    # 디코딩 진행
    decode_ais_file(file_path)

    # 디코딩 실패 항목 파일로 출력
    list_to_file('./data/error_data.txt', error_list)

    # 디코딩 결과 출력
    print("디코딩 실패 갯수:", len(error_list))
    print(dumps(error_count, indent=4))
