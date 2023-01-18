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



# decode 순서
- from pyais import decode
- decode(raw_data)
```python
def decode(*args: typing.Union[str, bytes]) -> ANY_MESSAGE:
    parts = tuple(msg.encode('utf-8') if isinstance(msg, str) else msg for msg in args)
    nmea = _assemble_messages(*parts)
    print(nmea)  # <- b'!AIVDM,1,1,,A,16S`fAP000a3OsLEKwfmKB:L0@8g,0*55'
    return nmea.decode()
```

- payload값(bit_array)과 ais_id(msgType) 가져오기
```python
# Finally decode bytes into bits
        self.bit_array: bitarray = decode_into_bit_array(self.payload, self.fill_bits)
        self.ais_id: int = get_int(self.bit_array, 0, 6)
```

```python
    def decode(self) -> "ANY_MESSAGE":
        """
        Decode the NMEA message.
        @return: The decoded message class as a superclass of `Payload`.

        >>> nmea = NMEAMessage(b"!AIVDO,1,1,,,B>qc:003wk?8mP=18D3Q3wgTiT;T,0*13").decode()
        MessageType18(msg_type=18, ...)
        """
        try:
            # self.bit_array => bitarray('000001000110100011101000101110010001100000000000000000000000101001000011011111111011011100010101011011111111101110110101011011010010001010011100000000010000001000101111')
            return MSG_CLASS[self.ais_id].from_bitarray(self.bit_array)  # <- MessageType1(msg_type=1, repeat=0, mmsi=257576000, status=<NavigationStatus.UnderWayUsingEngine: 0>, turn=0.0, speed=11.7, accuracy=True, lon=5.653795, lat=59.016863, course=137.9, heading=137, second=29, maneuver=0, spare_1=b'\x00', raim=False, radio=66617)
        except KeyError as e:
            raise UnknownMessageException(f"The message {self} is not supported!") from e
```

```python
    @classmethod
    def from_bitarray(cls, bit_arr: bitarray) -> "ANY_MESSAGE":
        cur: int = 0
        end: int = 0
        kwargs: typing.Dict[str, typing.Any] = {}

        # Iterate over the bits until the last bit of the bitarray or all fields are fully decoded
        for field in cls.fields():

            if end >= len(bit_arr):
                # All fields that did not fit into the bit array are None
                kwargs[field.name] = None
                continue

            width = field.metadata['width']
            d_type = field.metadata['d_type']
            converter = field.metadata['to_converter']

            end = min(len(bit_arr), cur + width)
            bits = bit_arr[cur: end]

            val: typing.Any
            # Get the correct data type and decoding function
            if d_type in (int, bool, float):
                shift = (8 - ((end - cur) % 8)) % 8
                if field.metadata['signed']:
                    val = from_bytes_signed(bits) >> shift
                else:
                    val = from_bytes(bits) >> shift
                val = d_type(val)
            elif d_type == str:
                val = decode_bin_as_ascii6(bits)
            elif d_type == bytes:
                val = bits2bytes(bits)
            else:
                raise InvalidDataTypeException(d_type)

            val = converter(val) if converter is not None else val

            val = cls.__force_type(field, val)
            kwargs[field.name] = val

            cur = end

        return cls(**kwargs)  # type:ignore
```