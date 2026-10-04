# TamaPoke v3.110.3 컴파일/UI 복구

최종 기준본: v3.110.1 RebuiltSprites FullSource Firmware

초기 v3.110.3은 손상된 v3.110.2 ZIP에서 복구한 변경본이었기 때문에 FullSource 원본 일부가 빠져 있었습니다.
이번 재이식본은 정상 v3.110.1 전체 소스를 기준으로 두고, v3.110.3에서 필요한 변경점만 선택적으로 다시 적용했습니다.

## 재이식한 변경점
- `ui_extra_sprites.h` 추가: TM 디스크 32px, 게임패드 24px, 쓰다듬기 24px.
- `assets/extra_sprites/`와 `tools/build_extra_sprites.py` 추가.
- `TamaPoke.ino` / `firmware_source/TamaPoke.ino`에 UI 스프라이트 표시 개선 및 FW_VERSION 3.110.3 적용.
- GitHub Actions를 명시적 clean build path로 변경.
- `file format not recognized` 객체 파일 링크 오류가 발생하면 build object를 제거하고 1회만 clean compile 재시도.
- 컴파일/링커 오류 로그에 `undefined reference`, `multiple definition`, `file format not recognized`를 함께 표시.
- 루트 OneClick Installer 버전 표기를 3.110.3으로 갱신.

## v3.110.1에서 그대로 보존한 항목
- `data/digimon/types.json`
- `assets/habitats/source/types/` 18타입 원본 전체
- `assets/habitats/source/sunset/bug.png`
- `assets/habitats/source/sunset/rock.png` 정상 원본
- `validation/info_sprites/` 전체
- `.github/workflows/main.yml`의 `tools/test_info_sprites.py` 검사
- `firmware_ready/` 전체

세이브 구조, 진화 데이터, 전투 규칙, 훈련 수치 등 게임 로직은 이번 재이식에서 별도로 변경하지 않았습니다.

## firmware_ready 주의
`firmware_ready/`의 `.bin` 및 `Install-v3.110.1.html`은 v3.110.1에서 만들어진 기존 사전 빌드 파일을 원본 보존 목적으로 유지한 것입니다.
v3.110.3 실기용 바이너리는 GitHub Actions에서 새로 컴파일해야 합니다.
