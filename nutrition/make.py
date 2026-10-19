# يجمع book.html من body.html وبيانات الوصفات
import html
from recipes import BREAKFAST, MAINS, SNACKS
CATS=[("فطور","s6-1",BREAKFAST),("غداء وعشاء","s6-2",MAINS),("سناك وحلى","s6-3",SNACKS)]
idx=['<ul class="rx-index split">']
rx=[]
for cat,sid,lst in CATS:
    idx.append(f'<li class="cat">{cat}</li>')
    for i,(rid,name,img,time,mac,serv,ing,steps,note) in enumerate(lst):
        idx.append(f'<li data-toc="{rid}"><a href="#{rid}">{name}</a><span class="kc">{mac[0]} سعرة</span><span class="pg"></span></li>')
        ings=''.join(f'<li{" class=opt" if "اختياري" in n else ""}><span class="q">{q}</span><span>{n}</span></li>' for q,n in ing)
        sts=''.join(f'<li>{s}</li>' for s in steps)
        nt=f'<div class="note rc-note"><b>ملاحظة</b>{note}</div>' if note else ''
        rx.append(f'''  <div class="pagebreak"></div>
  <article class="rc" id="{rid}">
    <figure class="rc-img"><img src="img/orig/{img}.webp" alt="{html.escape(name)}"></figure>
    <div class="rc-head"><div class="rc-cat">{cat} · {serv}</div><h2>{name}</h2><div class="rc-time">وقت التحضير: {time}</div></div>
    <dl class="rc-mac"><div><dd>{mac[0]}</dd><dt>سعرة</dt></div><div><dd>{mac[1]}<small>غ</small></dd><dt>بروتين</dt></div><div><dd>{mac[2]}<small>غ</small></dd><dt>كربوهيدرات</dt></div><div><dd>{mac[3]}<small>غ</small></dd><dt>دهون</dt></div></dl>
    <div class="rc-ing"><h3>المكوّنات</h3><ul>{ings}</ul></div><div class="rc-steps"><h3>الطريقة</h3><ol class="steps">{sts}</ol></div>
    {nt}
  </article>''')
idx.append('</ul>')
body=open('body.html').read().replace('<!--RXINDEX-->','\n'.join(idx)).replace('<!--RECIPES-->','\n'.join(rx))
head='''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>دليلك للتغذية — Nav Coaching</title>
<link rel="stylesheet" href="../source/fonts.css">
<link rel="stylesheet" href="../source/tokens.css">
<link rel="stylesheet" href="../source/styles.css">
<link rel="stylesheet" href="nutrition.css">
</head>
<body>
<div id="book"></div>
<div id="src">
'''
open('book.html','w').write(head+body+'\n</div>\n<script src="../source/paginate.js"></script>\n</body>\n</html>\n')
print('ok', sum(len(l) for _,_,l in CATS))
