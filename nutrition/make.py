# يجمع book.html من body.html وبيانات الوصفات
import html
import recipes as R

BASE = [("فطور","s6-1",R.BREAKFAST,None),("غداء وعشاء","s6-2",R.MAINS,None),("سناك وحلى","s6-3",R.SNACKS,None)]
SPECIAL = [
 ("لو كارب","s6-4",R.LOWCARB,"lowcarb","قليلة الكربوهيدرات (لو كارب)",
  "كل وصفة هنا فيها 15 غرام كربوهيدرات أو أقل للحصة. تناسب من يرتاح على كربوهيدرات أقل، أو يفضّل وجبة عشاء خفيفة النشويات.",
  "اللو كارب ليس أسرع في حرق الدهون إذا تساوت السعرات والبروتين؛ اختره لأنه يناسب شهيتك وروتينك، لا لأنه سحري. ولا تقلّل الخضار، فهي مصدر أليافك."),
 ("عالية البروتين","s6-5",R.HIPROTEIN,"protein","عالية البروتين",
  "30 غرام بروتين أو أكثر للحصة، والبروتين فيها يشكّل أكثر من ثلث السعرات. تسهّل عليك الوصول لاحتياجك اليومي، خصوصًا وقت التنشيف.",
  "وزّع بروتينك على 3–5 وجبات في اليوم بدل أن تأخذ أغلبه في وجبة واحدة."),
 ("مضادات الأكسدة","s6-6",R.ANTIOX,"antiox","غنية بمضادات الأكسدة",
  "مضادات الأكسدة مركّبات طبيعية في النباتات الملوّنة: التوت والرمان والسبانخ والجرجير والكركم والكاكاو والشاي الأخضر. تساعد الجسم على حماية خلاياه من الأكسدة الضارة.",
  "أفضل مصدر لها الأكل المتنوّع لا الكبسولات. المكمّلات العالية منها (مثل جرعات كبيرة من فيتامين C وE) لم تُثبت فائدة، وبعض الدراسات تشير إلى أنها قد تضعف تكيّف الجسم مع التمرين."),
 ("قليلة السعرات","s6-7",R.LOWCAL,"lowcal","قليلة السعرات",
  "250 سعرة أو أقل للحصة، وبحجم يشبع. مفيدة في أيام العجز، أو كوجبة خفيفة بين الوجبات.",
  "السر في الحجم: الخضار والشوربات والبروتين قليل الدهن تملأ المعدة بسعرات قليلة."),
 ("كثيرة السعرات","s6-8",R.HICAL,"hical","كثيرة السعرات (للتضخيم)",
  "600 سعرة أو أكثر للحصة. لمن يحتاج فائض سعرات ويصعب عليه يأكل كفايته.",
  "السعرات السائلة والأطعمة الكثيفة، مثل زبدة الفول السوداني والشوفان وزيت الزيتون والمكسرات، ترفع السعرات بدون شبع زائد."),
]
TAGNAME = {"lowcarb":"لو كارب","protein":"عالي البروتين","antiox":"مضادات أكسدة","lowcal":"قليل السعرات","hical":"كثير السعرات"}

def tags(rid, mac, home=None):
    k,p,c,f = mac
    t=set()
    if c<=15: t.add("lowcarb")
    if p>=30 and p*4/k>=0.33: t.add("protein")
    if k<=250: t.add("lowcal")
    if k>=600: t.add("hical")
    if rid in R.ANTIOX_EXISTING: t.add("antiox")
    if home: t.add(home)
    return [x for x in TAGNAME if x in t]

ALL=[]  # (cat, recipe, tags)
for cat,sid,lst,home in BASE: ALL += [(cat,r,tags(r[0],r[4])) for r in lst]
for cat,sid,lst,home,*_ in SPECIAL: ALL += [(cat,r,tags(r[0],r[4],home)) for r in lst]

def img_src(img): return f"img/{img}.webp" if img.startswith('gen/') else f"img/orig/{img}.webp"

def recipe_html(cat, r, tg):
    rid,name,img,time,mac,serv,ing,steps,note = r
    ings=''.join(f'<li{" class=opt" if "اختياري" in n else ""}><span class="q">{q}</span><span>{n}</span></li>' for q,n in ing)
    sts=''.join(f'<li>{s}</li>' for s in steps)
    nt=f'<div class="note rc-note"><b>ملاحظة</b>{note}</div>' if note else ''
    chips=''.join(f'<span class="chip">{TAGNAME[t]}</span>' for t in tg)
    return f'''  <div class="pagebreak"></div>
  <article class="rc" id="{rid}">
    <figure class="rc-img"><img src="{img_src(img)}" alt="{html.escape(name)}"></figure>
    <div class="rc-head"><div class="rc-cat">{cat} · {serv}</div><h2>{name}</h2><div class="rc-time">وقت التحضير: {time}</div><div class="rc-tags">{chips}</div></div>
    <dl class="rc-mac"><div><dd>{mac[0]}</dd><dt>سعرة</dt></div><div><dd>{mac[1]}<small>غ</small></dd><dt>بروتين</dt></div><div><dd>{mac[2]}<small>غ</small></dd><dt>كربوهيدرات</dt></div><div><dd>{mac[3]}<small>غ</small></dd><dt>دهون</dt></div></dl>
    <div class="rc-ing"><h3>المكوّنات</h3><ul>{ings}</ul></div><div class="rc-steps"><h3>الطريقة</h3><ol class="steps">{sts}</ol></div>
    {nt}
  </article>'''

def idx_li(r): return f'<li data-toc="{r[0]}"><a href="#{r[0]}">{r[1]}</a><span class="kc">{r[4][0]} سعرة</span><span class="pg"></span></li>'

idx=['<ul class="rx-index split">']
rx=[]
for cat,sid,lst,home in BASE:
    idx.append(f'<li class="cat">{cat}</li>')
    for r in lst:
        idx.append(idx_li(r)); rx.append(recipe_html(cat,r,tags(r[0],r[4])))
n=4
for cat,sid,lst,home,title,intro,tip in SPECIAL:
    idx.append(f'<li class="cat">{title}</li>')
    idx += [idx_li(r) for r in lst]
    others=[r for c,r,t in ALL if home in t and r not in lst]
    rx.append('  <div class="pagebreak"></div>')
    rx.append(f'  <h2 id="{sid}" class="rx-sec"><span class="k">6.{n}</span>{title}</h2>\n  <p class="lead">{intro}</p>\n  <div class="tip"><b>قبل أن تبدأ</b>{tip}</div>')
    rx.append('  <h3>وصفات هذا القسم</h3>\n  <ul class="rx-index one split">'+''.join(idx_li(r) for r in lst)+'</ul>')
    if others:
        rx.append('  <h3>وصفات أخرى في الكتيّب تناسب هذا الهدف</h3>\n  <ul class="rx-index one split">'+''.join(idx_li(r) for r in others)+'</ul>')
    for r in lst: rx.append(recipe_html(cat,r,tags(r[0],r[4],home)))
    n+=1
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
print('recipes', len(ALL))
for c,r,t in ALL: print(r[0], t)
