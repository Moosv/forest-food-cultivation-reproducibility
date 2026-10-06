# Version 1.0.0 verification

Tested locally on 2026-10-06 using Python 3.12.14 on Windows, with the package versions in `requirements.txt`.

## Actual workbook checks

The prepared six-sheet institutional workbook was read without modifying it. Its bibliographic, classification and decision records are not included in this repository. The institutional dataset URL is pending.

| Check | Result |
|---|---:|
| Detailed-review publications | 2,024 |
| Included / excluded / held | 1,590 / 282 / 152 |
| Forest-food unique publications | 47 |
| Forest-food crop links / crop groups | 50 / 12 |
| General-food unique publications | 697 |
| Comparator unique publications, including ginseng and other mushrooms | 745 |
| Food-linked unique publications | 792 |
| Publications with a recorded direct-experiment crop role | 1,008 |
| Record-recountable aggregate rows matched to workbook | 170 |

Period denominators were **41, 102, 289, 395, 600 and 163** for 2000–2004, 2005–2009, 2010–2014, 2015–2019, 2020–2024 and 2025 respectively. They sum to 1,590. The 2013 annual count was 73. The final period is one year, not five.

Figure 1 and Figure 2 were generated as 600 dpi JPEGs and visually inspected for readable labels, correct period denominators and absence of clipping. Their values are derived from the validated records. Exact image bytes can depend on platform and rendering libraries.

The original project entry points `python project.py validate` and `python project.py analyze` also passed in a temporary copy of the current project data and code, without rewriting historical source files. The new public scripts independently read the reduced Excel rather than those private project files.

## Tests

The 10 synthetic unit tests in `tests/test_analysis.py` passed. They cover unique-publication counting across multiple crops and production stages, year boundaries, multiple technology assignments, rounding, duplicate identifiers, orphan links, mismatched flags, invalid values/codes, frozen-snapshot checks and protection of existing output directories.

Additional in-memory checks on the actual workbook:

- Reversing the order of the stored aggregate rows still matched all 170 recounted rows.
- Changing an aggregate count, removing an aggregate row and duplicating an aggregate key were each rejected.

## What these checks do not establish

Six upstream search/screening counts are present only as reported summaries in the reduced workbook. Their arithmetic relationships were checked, but their source records were not recounted by the public code.

This verification establishes record-level consistency and agreement with the frozen classifications. It does not establish independent screening accuracy, reviewer agreement, complete full-text review, exhaustive search coverage or newly verified author affiliations. It does not certify that the institutional dataset has already been deposited.
