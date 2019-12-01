# 2-3-matching

### Requirements
* Python >= 3.5
  * PIP, virtualenv
  * networkx == 2.4

### Installation
#### ubuntu
```bash
sudo apt-get install python3-dev python3-pip
pip3 install virtualenv
```
#### windows
[릴리즈](https://github.com/YihanKim/2-3-matching/releases) 링크 참조.

### Usage
#### ubuntu
```bash
python3 src/main.py [match_type] [filepath]
```
#### windows
```console
main.exe [match_type] [filepath]
```
* 여기서 `match_type`은 2인조, 3인조 여부에 따라 2 또는 3으로 지정
* 아래의 입력 조건에 맞게 작성한 텍스트 파일 주소를 `filepath`에 입력

## 2-match
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
### Strategy(2-match)
* 모든 간선을 순회하여 발견되는 2-cycle을 매칭 처리
  * 각 정점의 out degree가 1 이하이므로 모든 2-cycle은 독립
* 남은 간선들 중 가능한 간선을 최대한(maximally) 매칭 처리
* 남은 정점들을 랜덤하게 매칭
* 성별에 따른 매칭 제약을 사용하지 않음

### Output(2-match)
* acceptance rate: 모든 간선(학생 간 지목한 총 숫자) 중에서 매칭에 반영된 비율
* Group 1, 2, ..., N/2 까지 두 학생의 ID를 리턴
* 출력 예시
```
Acceptance rate: 0.42857142857142855
Group 1: p1, p2
Group 2: p5, p4
Group 3: p8, p3
Group 4: p7, p6
```


## 3-match
### Input(3-match)
* 첫 번째 줄 입력 N, M은 각각 학생 수
* 두 번째 줄부터 N줄은 각각 2 ~ 3개의 값 입력
  * 2-match와 동일
* N+2줄부터 M줄은 같은 조가 될 수 없는 학생 ID 쌍을 입력
  * 예시. ID가 p3인 학생과 p4인 학생이 같은 조가 되어서는 안 될 때 - `p3 p4`
```
15 4
p1 M p2
p2 M p3
p3 F p1
p4 M p1
p5 M p6
p6 F p5
p7 F p8
p8 M p4
p9 F p7
p10 M p9
p11 F p10
p12 M p10
p13 M p10
p14 M p15
p15 F p5
p10 p7
p7 p4
p6 p15
p12 p13

```
### Strategy(3-match)
* 각 매칭의 제약
  * 구성원 셋의 성별이 모두 F이어서는 안 된다.
  * 그룹의 구성원 사이에 *같은 조가 되어선 안 되는 쌍*이 있어서는 안 된다.
* 우선 서로를 지목하는 3명(3-cycle)을 탐색하고 매칭 처리
  * 만약 3-cycle이 제약조건을 만족 못한다면 오류 반환
  * 3-cycle로 만들어진 구성원은 아래의 구성원 교환 대상이 아님
* 남은 인원 중 성별을 확인
  * 여성이 남성의 2배를 초과할 경우 제약조건을 만족할 수 없으므로 오류 반환
* 3명씩 묶어 성별을 균등하게 임의로 배정한 다음, 같은 조가 되어서는 안 되는 쌍을 추적
  * 랜덤한 다른 조와 구성원을 교환하여, 모든 조가 제약조건을 만족할 때까지 반복
* 지명도 반영률 최적화
  * 랜덤한 두 조의 구성원을 교환하여 지명도 반영률이 올라가면 현상 유지, 
  * 그렇지 않다면 구성원을 원상복귀

### Output(3-match)
* 출력 예시
```
Acceptance rate : 9 / 15 = 0.6
Group 1: p1, p2, p3
Group 2: p7, p14, p13
Group 3: p11, p8, p4
Group 4: p9, p12, p10
Group 5: p6, p5, p15
```

