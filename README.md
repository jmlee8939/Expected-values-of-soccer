## 축구경기 슛 기대득점 모델(xG)

### 주제

Expected Goals(xG) : 슈팅 상황을 고려하여 골이 들어갈 확률을 나타내는 값

- 축구 통계 회사 [Opta](https://www.statsperform.com/opta/) 에서 처음 소개된 이후 축구 분석에 널리 사용되고 있다. 
- 이를 실제 축구 경기 데이터를 활용하여 직접 구현해보았다.

### 데이터
[Statsbomb](https://github.com/statsbomb/open-data) 의 축구 경기 Event 데이터


### 모델링


Logistic Regression 모형 활용

$$y = f(X)$$

<br>

$y$ : 골이 될 확률 
<br>
$\mathbf{X} = [X_0,X_1,X_2, ...]$ : 슈팅 상황

<br>

슈팅 상황 $X_i$ Feature : 
- 슈팅지점과 골라인 가운데 점 사이의 거리
- 슈팅지점과 양쪽 포스트 사이의 각도
- 슈팅 타입(왼발, 오른발, 그 외)
- 슈팅 상황(Open play, 페널티킥, 프리킥)
- 어시스트 패스 여부
- 어시스트 패스 높이(땅볼, 낮게, 높게)

<br>


### 샘플 데이터

||
|--|
|<img src="https://github.com/jmlee8939/jmlee8939.github.io/assets/58785929/8d9703a7-c091-4020-85a2-1de2a35fedba" width="300" height="200"/>|

### 모델 검증

|샘플 데이터의 예측결과| 모델의 AUC-ROC|
|--|--|
|<img src="https://github.com/jmlee8939/jmlee8939.github.io/assets/58785929/2fbddfb2-6d68-4e36-bbdf-a925d88ce657" width="300" height="200"/>|<img src="https://github.com/jmlee8939/jmlee8939.github.io/assets/58785929/ce947773-9670-41ae-bd58-2b9e3f91e9e0" width="300" height="200"/>|




