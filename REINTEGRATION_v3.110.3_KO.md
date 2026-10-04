# TamaPoke v3.110.3 변경점 재이식 복구본

기준: v3.110.1 RebuiltSprites FullSource Firmware

이 복구본은 손상된 v3.110.2를 기준으로 만들었던 초기 v3.110.3을 기준본으로 사용하지 않고,
정상 v3.110.1 FullSource에 v3.110.3의 필요한 변경점만 다시 이식했다.

## 보존한 v3.110.1 원본
- data/digimon/types.json
- assets/habitats/source/types/ 18타입 전체 원본
- assets/habitats/source/sunset/bug.png
- assets/habitats/source/sunset/rock.png (time_manifest.json과 일치하는 정상 원본)
- validation/info_sprites/
- firmware_ready/ 전체 (v3.110.1 사전 빌드 바이너리/설치기)
- GitHub Actions의 tools/test_info_sprites.py 검증 단계

## 재이식한 v3.110.3 변경점
- ui_extra_sprites.h
- TM 디스크 / 게임패드 / 쓰다듬기 UI 스프라이트
- 관련 assets/extra_sprites 및 build_extra_sprites.py
- TamaPoke.ino / firmware_source/TamaPoke.ino UI 적용 및 FW_VERSION 3.110.3
- GitHub Actions clean build + 객체 파일 형식 오류 1회 자동 재시도
- 루트 OneClick Installer 버전 표기 3.110.3

## 주의
firmware_ready/ 안의 .bin과 Install-v3.110.1.html은 v3.110.1에서 생성된 기존 사전 빌드 파일을
원본 보존 목적으로 그대로 유지했다. v3.110.3 실기 펌웨어는 GitHub Actions에서 새로 컴파일해야 한다.
