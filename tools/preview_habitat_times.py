from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,base64
R=Path(__file__).resolve().parents[1];D=R/'previews/time';D.mkdir(parents=True,exist_ok=True)
names='normal fire water electric grass ice fighting poison ground flying psychic bug rock ghost dragon dark steel fairy'.split()
labels='노말 불꽃 물 전기 풀 얼음 격투 독 땅 비행 에스퍼 벌레 바위 고스트 드래곤 악 강철 페어리'.split()
phases=['day','sunset','night'];data={};mask=Image.new('L',(466,466));ImageDraw.Draw(mask).ellipse((0,0,465,465),fill=255)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
for n in names:
 data[n]={};sheet=Image.new('RGB',(1438,514),'#101824');dr=ImageDraw.Draw(sheet)
 for i,p in enumerate(phases):
  path=R/'assets/habitats/runtime'/('' if p=='day' else p)/(n+'.png');small=Image.open(path).convert('RGB');pixels=small.load();out=Image.new('RGB',(466,466));out.putdata([pixels[x*116//466,y*116//466] for y in range(466) for x in range(466)])
  out.save(D/f'{n}_{p}_466.png');data[n][p]='data:image/png;base64,'+base64.b64encode((D/f'{n}_{p}_466.png').read_bytes()).decode()
  circle=Image.new('RGB',(466,466),'#101824');circle.paste(out,(0,0),mask);sheet.paste(circle,(i*480,0));dr.text((i*480+15,481),n.upper()+' / '+p.upper(),font=font,fill='white')
 sheet.save(D/(n+'_comparison.png'))
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>TamaPoke 시간별 배경 미리보기</title><style>body{font-family:system-ui;background:#101824;color:#f4f7ff;margin:32px auto;max-width:1050px;padding:0 20px}select,input{font-size:18px;padding:8px}#main{display:block;width:min(466px,100%);border-radius:50%;margin:24px auto;image-rendering:pixelated}.row{display:flex;gap:12px}.row figure{margin:0;flex:1;text-align:center}.row img{width:100%;border-radius:50%;image-rendering:pixelated}p{line-height:1.6}label{display:inline-block;margin-right:24px}</style><h1>시간에 따라 달라지는 서식지</h1><p>v3.109.0 · 실제 실행용 16색 배경을 466×466으로 표시합니다. UI·캐릭터·날씨 효과를 제외한 배경 미리보기이며, 실기 화면 캡처가 아닙니다.</p><label>타입 <select id="type"></select></label><label>기기 시각 <input id="hour" type="range" min="0" max="23" value="18"><output id="clock"></output></label><img id="main"><div class="row"><figure><img id="day"><figcaption>낮 · 06:00–16:59</figcaption></figure><figure><img id="sunset"><figcaption>노을 · 17:00–19:59</figcaption></figure><figure><img id="night"><figcaption>밤 · 20:00–05:59</figcaption></figure></div><p>기기에 설정된 시계를 따릅니다. 배경은 각 시간 구간에서 정지 이미지로 표시되며, 경계 시각에 화면 전체가 전환됩니다. 기존 날씨 효과는 유지됩니다.</p><script>const data=DATA,labels=LABELS;const select=document.getElementById('type'),hour=document.getElementById('hour');Object.keys(data).forEach((n,i)=>select.add(new Option(labels[i],n)));select.value='water';function update(){const h=+hour.value,p=h<6||h>=20?'night':h>=17?'sunset':'day',d=data[select.value];document.getElementById('clock').value=String(h).padStart(2,'0')+':00';document.getElementById('main').src=d[p];['day','sunset','night'].forEach(p=>document.getElementById(p).src=d[p]);}select.onchange=hour.oninput=update;update();</script></html>'''
(R/'TIME_BACKGROUNDS_PREVIEW.html').write_text(html.replace('DATA',json.dumps(data)).replace('LABELS',json.dumps(labels,ensure_ascii=False)))
print('18 comparison sheets + standalone offline preview')
for phase in phases:
 sheet=Image.new('RGB',(3*250,6*276),'#101824');dr=ImageDraw.Draw(sheet)
 for i,n in enumerate(names):
  im=Image.open(D/f'{n}_{phase}_466.png').resize((232,232),Image.Resampling.NEAREST)
  x=i%3*250;y=i//3*276;sheet.paste(im,(x+9,y));dr.text((x+10,y+240),n+' / '+phase,font=font,fill='white')
 sheet.save(D/(phase+'_all18.png'))
