# 2-3-match

### Requirements
* Python >= 3.5
  * PIP, virtualenv

### Installation
##### ubuntu
```console
sudo apt-get install python3-dev python3-pip
pip3 install virtualenv
```
##### windows 
다운로드 링크 참조.

### Usage
##### ubuntu
```console
python3 src/main.py [match_type] [filepath]
```
##### windows
```console
main.exe [match_type] [filepath]
```
* 여기서 `match_type`은 2인조, 3인조 여부에 따라 2 또는 3으로 지정
* 아래의 입력 조건에 맞게 작성한 텍스트 파일 주소를 `filepath`에 입력

### Input(2-match)
* 첫 번째 줄 입력 N은 학생 수
* 두 번째 줄부터 N줄은 각각 2 ~ 3개의 값 입력
  * 첫 번째 값은 학생의 ID
  * 두 번째 값은 성별(남성 - M, 여성 - F)
  * 세 번째 값은 학생이 지목한 다른 학생의 ID (없어도 무방)
  * 예시. ID가 p1인 남학생이 ID가 p2인 학생을 지목 - `p1 M p2`
* 입력 파일 예시
  * 주의 - 마지막 줄 입력 후 개행 문자 필요
```
8
p1 M p2
p2 M p1
p3 M 
p4 M p1
p5 M p4
p6 M p5
p7 M p4
p8 M p2

```

### Output(2-match)
* acceptance rate: 모든 간선(학생 간 지목한 총 숫자) 중에서 매칭에 반영된 비율
* Group 1, 2, ..., N/2 까지 두 학생의 ID를 리턴
* 출력 예시
```

```


### Input(3-match)
* 첫 번째 줄 입력 N, M은 각각 학생 수 
* 두 번째 줄부터 N줄은 각각 2 ~ 3개의 값 입력
  * 2-match와 동일
* N+2줄부터 M줄은 같은 조가 될 수 없는 학생 ID 쌍을 입력
  * 예시. ID가 p3인 학생과 p4인 학생이 같은 조가 되어서는 안 될 때 - `p3 p4`


