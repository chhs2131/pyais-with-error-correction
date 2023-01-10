## 기능 목록
### NMEA 형식 확인 - NvmeCheck
  - [ ] NMEA 포맷 검증 - validateNvmeFormat
    - 쉼표가 7개인지 확인한다.
  - [ ] NMEA 포맷으로 복구하는 기능 - repairNvmeFormat**
    - 정상 포맷인 쉼표 7개 형태로 만들기
  - [ ] NMEA 메세지 통계값을 확인 - statsNvme
    - 결측치, 민맥스, 형식, … 값 등을 확인
    - 통계값을 출력 - printNvmeStats

### 다중메세지 처리 - MultiSequenceNvme
  - [ ] 다중메시지인지 확인하기 - isMultiSequenceNvme
  - [ ] 다중메세지를 Queue에 넘김 - tossToQueue**
    - 메세지가 완성된경우 반환값을 받게됨

### 다중 메세지들을 처리할 queue - MultiSequenceQueue
- [ ] queue 대기자 명단에 신규 등록 - addMessage
- [ ] 전체 시퀀스가 완성된 경우 디코딩 진행 - checkSequenceQueue
  - [ ] 이미 동일한 시퀀스 메세지가 queue에 있는지 확인 - isSequenceComplete
  - [ ] 세트 메세지들을 추출해서 하나의 list로 만든다. - listCompleteMlutiMessage
  - [ ] 세트 메세지를 디코딩한다. - decodeMultiMessage

### Payload 제어 - payloadController
  - [ ] NMEA 메세지에서 Payload만 추출하기 - getPayload
  - [ ] Payload 검증 - validatePayload
  - [ ] MMSI 검증 - validateMmsi
  - [ ] 각 메세지 타입별 주요 데이터만 추출하기 - getImportantColumn**

### 메세지 타입별 컬럼 정보 저장 - MsgType
- [ ] 각 메세지 타입별 컬럼을 저장해둔다.
- [ ] 각 메시지 타입별 중요도있는 컬럼 체크
- [ ] 각 메세지 타입별 데이터 추출

## 기타
- [ ] RAW DATA 확보
- [ ] 체크섬 복구여부 결정
- [ ] 이후 기존 오픈소스와 융합
- [ ] 정제된 LIST를 반환하기

---

# 발견된 문제점

### 멀티메세지
- [x] 시퀀스넘버가 0번으로 오는 경우
- [ ] [MULTI] Missing fragment numbers: [2] !AIVDM,2,1,0,A,56SgAOPIVIVKK3L0000@4F0eUDpN0Pt00000000000000400000000000000,0*6B

### 형식문제
- [x] [E_FORMAT] Invalid character: *42 !AIVDM,1,1,,B,16S`1lP0h093mGrEGj89BbiF,2,9,A,00000000000,2*2D

