# 시설재배·숲푸드자원 문헌분석 재현 코드

**Code for reproducing publication counts and figures for protected cultivation and forest-food resource research in Korea, 2000–2025**

Version **1.0.0**. 분석기간은 출판연도 **2000–2025년**이며, 최종 포함 **1,590편**, 숲푸드자원 **47편**을 대상으로 합니다. 공개용 Excel에 이미 기록된 분류를 재집계하는 코드입니다. 검색·AI 선별·원문 검토를 다시 수행하지 않습니다.

## 자료와 코드의 구분

- **과학원 DB**: 문헌목록, 기술·작목 분류, 시설재배 분류 근거, 2,024편의 최종 선정 결과와 기록된 근거, 집계표.
- **이 저장소**: Excel 입력, 고유 문헌 수·비율 집계, 그림 1·2 작성, 기록 간 일관성 검사, 실행 안내와 테스트.

**데이터 등록 URL: 아직 연결되지 않았습니다.** 과학원 DB 등록 후 이 항목에 공식 데이터셋 URL과 버전을 추가할 예정입니다. GitHub 코드의 공개는 데이터셋의 공식 등록을 의미하지 않습니다. 실제 문헌자료·AI 로그·원문·원고·비공개 개발 이력은 이 저장소에 포함하지 않습니다.

## 입력 Excel

과학원 DB에 등록할 `과학원DB_문헌분석자료_2000-2025_공개용간소화.xlsx` 형식의 단일 파일을 사용합니다. 아래 시트의 데이터는 첫 행에 영문 필드명, 둘째 행부터 기록이 위치합니다. 파일명과 보관 경로는 바꿔도 되지만 시트명·필드명은 유지해야 합니다.

| 시트 | 내용 | 데이터 행 수 |
|---|---|---:|
| 자료이용안내 | 자료 정의·코드 설명; 집계 입력에서는 제외 | — |
| 분석문헌과기술분류 | 고유 문헌과 기술 코드 | 1,590 |
| 숲푸드문헌과분류근거 | 숲푸드 문헌과 시설재배 분류 근거 | 47 |
| 문헌별작목분류 | 문헌–작목 연결 | 1,283 |
| 문헌선정결과와근거 | 포함·제외·보류 결과와 기록된 근거 | 2,024 |
| 분석집계결과 | 기록 단위 재집계와 대조할 기존 집계값 | 176 |

상세 필드 설명은 Excel의 `자료이용안내`에 있습니다. `work_id`는 문헌 식별자, `target_id`는 문헌–작목 연결 식별자입니다. 빈 값은 0이나 false로 대체하지 않습니다. 논리값은 `true`/`false`, 기술·생산과정 코드는 JSON 배열 문자열(예: `["T1", "T2"]`)로 읽습니다. 수식·오류 셀은 데이터 시트에서 허용하지 않습니다.

## 실행

Python 3.12 환경에서 검증했습니다. 명령은 이 저장소 폴더에서 실행합니다. `data/input.xlsx`는 사용자가 내려받은 실제 Excel 파일의 경로로 바꾸세요. 실제 자료가 없으면 입력 부재 오류로 종료됩니다.

```sh
python -m pip install -r requirements.txt
python check_data.py --input "data/input.xlsx"
python reproduce_analysis.py --input "data/input.xlsx" --output-dir "results-v1" --figures
```

그림만 별도로 생성하려면:

```sh
python make_figures.py --input "data/input.xlsx" --output-dir "figures-v1"
```

출력 폴더는 **존재하지 않는 새 경로**로 지정합니다. 기존 파일과 원본 Excel을 덮어쓰지 않습니다. 실행 시 네트워크, API 키, AI 모델 또는 비공개 개발 자료는 필요하지 않습니다. 최초 패키지 설치와 데이터 다운로드에는 네트워크가 필요할 수 있습니다.

검사에 실패하면 결과를 새로 만들지 않습니다. 검사를 통과한 뒤 디스크·렌더링 오류가 발생하면 일부 출력만 남을 수 있으므로 종료 코드와 `validation_report.json`을 함께 확인하세요.

## 집계 규칙

1. 집계 단위는 고유 `work_id`입니다. 한 문헌이 여러 작목·기술에 해당할 수 있어 항목별 합계는 전체 고유 문헌 수와 다를 수 있습니다. 여러 작목을 합칠 때는 식별자 집합의 합집합으로 셉니다.
2. 기술별 주 분석은 `research_focus_codes`의 T1–T8을 사용합니다. 전체 비율의 분모는 1,590편, 기간별 비율의 분모는 해당 기간의 전체 포함 문헌입니다. 비율은 `round(100 * n / denominator, 1)`입니다. 복수 기술을 허용하므로 합계가 100%일 필요는 없습니다.
3. `focus_or_core_codes`는 별도의 초점·핵심구현 집계에 사용하며 주 분석 코드를 대체하지 않습니다. OT는 원자료에서 유지하지만 T1–T8 표·그림에는 포함하지 않습니다.
4. 기간은 2000–2004, 2005–2009, 2010–2014, 2015–2019, 2020–2024, **2025 단일 연도**입니다. 마지막 구간은 5년 구간과 길이가 다릅니다.
5. 숲푸드자원은 `forest_named`, `forest_mushroom`, `forest_author_confirmed`의 합집합입니다. 12작목, 연결 50건, 고유 문헌 47편입니다. 경계 사례(`forest_boundary` 등)는 자동으로 포함하지 않습니다.
6. 비교집합은 `common_food_crop`, `ginseng_comparator`, `mushroom_comparator`의 합집합 745편입니다. 그중 `common_food_crop`만의 고유 문헌 수는 697편입니다. 원자료 집계표의 **‘일반 먹거리 작목’ 행 그룹은 인삼·기타 버섯 비교군을 포함**합니다. 이름만 보고 697편 집합으로 해석하지 마세요. 비교집합과 숲푸드자원을 합친 먹거리 연결 문헌은 792편입니다.
7. 생산과정별 집계도 숲푸드 문헌의 고유 식별자로 셉니다. 이는 기록된 연구 분포이며, 작목별 성과·기술 수준을 점수화한 평가가 아닙니다.

## 출력

| 파일 | 의미 |
|---|---|
| `annual_counts.csv` | 2000–2025년 연도별 문헌 수, 26행 |
| `technology_counts.csv` | T1–T8 연구초점 수·비율과 초점·핵심구현 수, 8행 |
| `period_technology.csv` | 6기간 × 8기술 수·분모·비율, 48행 |
| `crop_counts.csv` | 작목별 고유 문헌 수, 73행 |
| `forest_production_stages.csv` | 숲푸드 연구의 생산과정별 고유 문헌 수, 8행 |
| `selection_counts.csv` | 공개 기록에서 재집계한 최종 선정·부분집합 수, 7행 |
| `validation_report.json` | 집계값, 입력 SHA-256, 검사 범위와 한계 |
| `Figure1_annual_publications_1590.jpg` | 연도별 문헌 수, 600 dpi |
| `Figure2_period_technology_1590.jpg` | 기간 내 기술별 문헌 비율, 600 dpi |

CSV는 Excel에서 한글을 읽기 쉬운 UTF-8 BOM 형식입니다. 출력물은 GitHub에 자동 업로드되지 않습니다.

## 검증 범위와 한계

식별자 중복·연결, 출판연도, 선정 집합, 숲푸드/먹거리 플래그, 분류 코드, 실제 기록에서 재계산한 **170개 집계 행**을 확인합니다. 기준 집합이 달라지면 다른 연구 버전으로 보고 오류를 냅니다. 이 코드는 임의의 신규 문헌집합을 분석하는 범용 선별기가 아닙니다.

최초 검색·중복 병합·서지 제외·내용 심사·상세검토 미선정에 관한 **6개 상류 집계값은 원자료가 이 축약 Excel에 없으므로 다시 세지 않습니다.** `validation_report.json`의 `reported_upstream_counts_not_recounted`에 기록값으로 구분하고, 값 사이의 산술 관계만 확인합니다. 따라서 출력 `selection_counts.csv`는 Excel에 기록된 선정 집계 13행 전체의 복제본이 아닙니다.

일관성 검사 통과는 연구자의 판정 정확도, 문헌검색의 완전성, 국내 기관 소속의 전수 확인, 검토자 간 일치도 또는 전체 원문 검토의 완료를 입증하지 않습니다. 근거 필드는 기존 기록을 보존한 것이며 코드가 새 근거를 만들어 내지 않습니다.

## 테스트

실제 문헌 없이 실행할 수 있는 소규모 합성자료 테스트:

```sh
python -m unittest discover -s tests -v
```

릴리스 전 실제 공개용 Excel을 이용해 위 집계와 그림을 확인했습니다. 상세 결과는 [검증 기록](VERIFICATION.md)을 참고하세요. 재실행 보고서의 SHA-256은 사용자가 실제 입력한 파일을 식별합니다. Excel 파일을 재저장하면 값이 같아도 파일 해시가 바뀔 수 있습니다.

## 논문에서 인용

코드 인용은 저장소 첫 화면보다 **논문 계산에 사용한 버전의 URL**을 사용합니다. 본문 예시:

> 공개 분석자료의 문헌 수와 비율을 집계하고 그림을 재생성하는 Python 코드를 제공하였다(코드 작성자, 2026).

참고문헌 형식 예시(작성자명은 실제 기여자와 기관 확인 후 기입):

> [Code author(s)]. 2026. Code for reproducing publication counts and figures for protected cultivation and forest-food resource research in Korea, 2000–2025. Version 1.0.0. GitHub. https://github.com/Moosv/forest-food-cultivation-reproducibility/tree/v1.0.0

데이터와 코드는 별도로 인용합니다. 위 연도는 코드 공개연도이며 문헌 분석기간의 상한은 2025년입니다.

## 이용조건

기관 정책과 권리자 확인 전까지 별도의 오픈소스 라이선스를 지정하지 않았습니다. 공개 열람 가능 상태와 재사용 라이선스 부여는 구분됩니다. 데이터 이용조건은 과학원 DB의 데이터셋 안내를 따릅니다.

## English summary

This repository recounts the frozen classifications in a single six-sheet institutional Excel workbook. It reproduces annual, technology, crop and production-stage summaries and two figures for 1,590 publications (2000–2025), including 47 forest-food publications. It does not rerun search or AI screening. The dataset is not included; its institutional deposit URL is pending. Record consistency and aggregate agreement are not evidence of independent screening accuracy or full-text eligibility validation. No open-source license has yet been assigned.
