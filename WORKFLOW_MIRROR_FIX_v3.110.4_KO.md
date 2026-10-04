# TamaPoke v3.110.4 Workflow Mirror Fix

기준: v3.110.3 Reintegrated FullSource

## 수정 내용
- `.github/workflows/main.yml`과 `GITHUB_WORKFLOW_COPY.txt`를 바이트 단위로 동일하게 동기화.
- v3.110.3 재이식 과정에서 실제 workflow에만 복원되었던 `tools/test_info_sprites.py` 검증 한 줄을 mirror에도 반영.
- `tools/verify_catalog_push_resilience.py`의 `workflow mirror drift` 실패 해결.
- 펌웨어/설치기 버전 표기를 3.110.4로 갱신.

## 변경하지 않은 내용
- 세이브 구조
- 진화/조그레스 로직
- 전투/훈련/기력 로직
- 18타입 낮/노을/밤 배경 이미지 및 시간 전환 로직
- UI 스프라이트 이미지 데이터
- 기존 v3.110.1에서 보존한 FullSource 원본 및 validation/firmware_ready 자료

## 주의
`firmware_ready/` 안의 기존 바이너리는 보존용 v3.110.1 산출물입니다. v3.110.4 실기용 바이너리는 GitHub Actions에서 새로 컴파일해야 합니다.
