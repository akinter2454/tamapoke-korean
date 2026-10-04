from pathlib import Path

root=Path(__file__).resolve().parents[1]
wf=(root/'.github/workflows/main.yml').read_text(encoding='utf-8')
copy=(root/'GITHUB_WORKFLOW_COPY.txt').read_text(encoding='utf-8')

assert wf == copy, 'workflow mirror drift'
assert 'Commit generated catalog lock source (best effort)' in wf
assert 'continue-on-error: true' in wf
assert 'git fetch origin "${GITHUB_REF_NAME}" || true' in wf
assert 'REMOTE_HEAD="$(git rev-parse "origin/${GITHUB_REF_NAME}"' in wf
assert 'Skipping generated catalog source commit; deployment will continue.' in wf
assert 'Generated catalog push was rejected' in wf
assert 'Pages deployment will continue.' in wf
print('catalog push resilience OK: generated source push cannot block Pages deployment')
