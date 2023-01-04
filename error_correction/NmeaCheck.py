# !AIVDM,1,1,,A,16Sd0KUq1o93PMbEG=T3Pi>L0<7E,0*0F
# 포맷을 확인하여 각 로직으로 전달하는 역할
# 정상 메세지 -> 디코딩 로직
# 멀티 메세지 -> 멀티메세지 큐 -> 디코딩 로직
# 포맷이상 메세지 -> Payload 추출 -> 전용 decode 로직 -> 추가로 검증도 필요

import re

class NvmeCheck:
    def validateNvmeFormat(self, string):
        count = string.count(',')
        if string.count(',') != 6:
            # 마지막 4글자가 0*00 형태일 경우
            if re.search('\d\*\d\d$', string):  # 끝에 4글자 또는 쉼표포함 5글자를 제거한 후에 가장 뒤에있는 BLOCK을 가져오면 Payload만 가져오는 것이 된다.
                raise ValueError("========>")

            if count == 5:  # 가장 뒤에 블럭 추출
                raise ValueError("555555555555555")
            if count == 7:
                raise ValueError("777777777777777")
            raise ValueError("jjjjjjjjjjjjjjjj")

        nmea = string.split(',')
        if len(nmea) < 4:
            raise ValueError("해석하기에는 너~무 작은 메시지")  # 복구 불가능한 케이스
        if nmea[1] != '1':
            raise ValueError("멀티메세지!")

        return True  # 정상 메세지

    def repairNvmeFormat(self, string):
        # 쉼표를 기준으로 데이터를 나눈다.
        data = string.split(',')

        # 7개이지만 에러가 나는 경우에 복구
        # i = 0
        # for d in data:
        #     if i == 0 and d != '!AIVDM':
        #         d = '!AIVDM'
        #     if i == 1 and
        #     i += 1

        pass

    def statsNvme(self):
        pass


if __name__ == '__main__':
    nvmeCheck = NvmeCheck()

    # RAW DATA 파일 불러오기
    file_path = './data/ais_20211104_15.txt'

    with open(file_path) as f:
        lines = f.readlines()
        for msg in lines:
            data = msg
            try:
                nvmeCheck.validateNvmeFormat(data)
            except Exception as e:
                print(e, data)
                # if str(e) == "A NMEA message needs to have exactly 7 comma separated entries.":  # 특정 예외만 표출 처리
                #     print(data)
                # traceback.print_exc()
                ## error_count[str(e)] += 1
                ## error_list.append(data)
                # print(f'[ERROR] Value {data} not in JSON/AIS format')

    '''
    # 디코딩 결과 출력
    print("디코딩 실패 갯수:", len(error_list))
    print(dumps(error_count, indent=4))
    '''