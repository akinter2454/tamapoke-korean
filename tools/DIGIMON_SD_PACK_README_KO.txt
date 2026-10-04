TamaPoke v3.90.0 디지몬 SD 팩 만들기

권장 변환기
- tools/Digimon-SD-Pack-Maker.html
- 독립 파일: tools/Digimon-Pendulum-DMUL-SD-Pack-Maker-v3.87.0.html
- Chrome/Edge에서 인터넷·Python 없이 실행됩니다.

지원 그룹
- DMC Ver.1~5
- Pendulum P0~P5
- DMUL 6 DigiTama: Dragon / Dark / Deep / Nature / Nightmare / Secret
- DMUL 추가분은 유년기 I/II 13종 + 성장기 이상 37종 = 50종입니다.

일괄 변환
- dmc1~dmc5, p0~p5 또는 DMUL 폴더 아래 캐릭터별 ZIP을 넣은 바깥 ZIP을 선택합니다.
- 캐릭터별 ZIP이 0.png~14.png의 48x48 프레임을 가지면 DGI3 15프레임으로 변환합니다.
- 기존 단일 PNG/3프레임 시트 변환도 유지합니다.
- 결과 ZIP의 digimon 폴더를 SD 카드 최상위에 복사합니다.
- /mons는 포켓몬 전용이므로 그대로 둡니다.

DMUL 파일명 별칭
- Growlmon→Growmon, MegaGrowlmon→MegaloGrowlmon
- Gallantmon→Dukemon, Diaboromon→Diablomon
- DoruGreymon→DORUguremon, Hisharyumon→Hisyaryumon 등 주요 영문명 차이를 자동 대응합니다.

DGI3
- RGB565-LE, 투명 0x0001, 검정 0x0000
- 48x48, 3 또는 15프레임
- 생성 직후 헤더/크기/프레임/RGB565를 다시 검증합니다.

원본 PNG와 변환된 .dgi는 GitHub 저장소에 포함하지 않습니다.

DMUL 원본 수집 도구
- tools/DMC-DMUL-Required-Sprite-Downloader.html
- DMC Sprite Database가 사용하는 공개 tero0x/dmc-sprites/sprites.json을 온라인에서 읽습니다.
- Source=DMUL만 필터링하고 TamaPoke DMUL 50종만 기본 선택합니다.
- 같은 종의 후보가 여러 개면 항목을 고른 뒤 선택 파일만 ZIP으로 받을 수 있습니다.
- 온라인 자동 로드가 막히면 sprites.json을 직접 선택하는 로컬 fallback을 제공합니다.
- 이 도구는 원본 스프라이트를 프로젝트에 내장하지 않습니다.

DMUL 진화 분기
- 공격/방어/스피드/체력 중 가장 많이 훈련한 능력치가 분기를 결정합니다.
- 동률은 해당 디지몬의 자연 style이 동률 후보일 때 우선하고, 이후 ATK>DEF>SPE>HP 순입니다.
- 돌봄 실수는 진화 결과를 고르지 않고 기존처럼 진화 시기 지연에만 사용합니다.
