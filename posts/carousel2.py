# الكاروسيل v2 — ٨ شرائح بالصور: غلاف + ٦ شرائح (بديلان لكل شريحة) + قواعد + دعوة
HEAD='''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><link rel="stylesheet" href="../source/fonts.css"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#0B1734;font-family:"IBM Plex Sans Arabic";color:#fff;position:relative;overflow:hidden}
h1,h2,.n,.k{font-family:"Readex Pro"}
.top{position:absolute;top:56px;right:64px;left:64px;display:flex;align-items:center;justify-content:space-between}
.top img{height:54px}.pg{font:600 26px "Readex Pro";color:#1FBAEC;letter-spacing:2px}
.ttl{position:absolute;top:140px;right:64px;left:64px;font:700 58px/1.25 "Readex Pro"}
.ttl span{color:#1FBAEC}
.row{position:absolute;right:48px;left:48px;height:400px;border-radius:36px;overflow:hidden;display:flex;background:#132650}
.half{position:relative;flex:1;overflow:hidden}
img[src*="fries"]{object-position:95% 40%!important}
.half img{width:100%;height:100%;object-fit:cover;display:block}
.bad img{filter:saturate(.55) brightness(.75)}
.half::after{content:"";position:absolute;inset:0;background:linear-gradient(transparent 45%,rgba(6,14,36,.92))}
.cap{position:absolute;bottom:28px;right:28px;left:28px;z-index:2}
.tag{display:inline-block;font:700 22px "Readex Pro";padding:6px 18px;border-radius:40px;margin-bottom:10px}
.bad .tag{background:#E5484D}.good .tag{background:#1FBAEC;color:#0B1734}
.k{font-size:40px;font-weight:700;line-height:1.2}
.cal{font:600 26px "IBM Plex Sans Arabic";opacity:.9;margin-top:4px}
.arrow{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:3;width:92px;height:92px;border-radius:50%;background:#fff;color:#284DA0;display:grid;place-items:center;font:700 52px "Readex Pro";box-shadow:0 8px 30px rgba(0,0,0,.35)}
.why{position:absolute;right:48px;left:48px;font-size:27px;line-height:1.5;color:#BFD0EE;padding:0 12px}
.why b{color:#fff}
.foot{position:absolute;bottom:40px;right:64px;left:64px;display:flex;justify-content:space-between;font:500 24px "Readex Pro";color:#7F93BD}
</style></head><body>'''
LOGO='<img src="../source/img/logo-white-cyan.png" alt="Nav Coaching">'
def top(i): return f'<div class="top">{LOGO}<span class="pg" dir="ltr">{i:02d} / 08</span></div>'
FOOT='<div class="foot"><span>navcoaching.com</span><span>اسحبي ←</span></div>'
def half(cls,img,tag,name,cal):
    return f'<div class="half {cls}"><img src="img/{img}.jpg"><div class="cap"><span class="tag">{tag}</span><div class="k">{name}</div><div class="cal">{cal}</div></div></div>'
def row(y,s):
    b,g=s
    return (f'<div class="row" style="top:{y}px">'+half('bad',b[0],'بدل',b[1],b[2])+half('good',g[0],'البديل',g[1],g[2])+'<div class="arrow">←</div></div>')
def why(y,t): return f'<div class="why" style="top:{y}px">{t}</div>'

SW=[  # (سيئ, جيد, ملاحظة)
 (('fries','بطاطس مقلية','≈ 365 سعرة'),('baked','بطاطس بالفرن','≈ 160 سعرة'),'<b>نفس الطعم المقرمش</b> — قطّعيها أصابع، رشة زيت وبابريكا، ٢٥ دقيقة بالفرن.'),
 (('fried_chicken','دجاج مقلي','≈ 360 سعرة'),('grilled_chicken','دجاج مشوي','≈ 190 سعرة'),'<b>البروتين نفسه بنصف السعرات</b> — تتبيلة لبن وليمون وبهارات تكفي.'),
 (('soda','مشروب غازي','≈ 140 سعرة'),('sparkling','ماء فوار بليمون','0 سعرة'),'<b>تبغين الفوران؟</b> خذيه بدون ٩ ملاعق سكر.'),
 (('mayo','مايونيز','≈ 190 سعرة / ملعقتين'),('yogurt','زبادي يوناني','≈ 30 سعرة / ملعقتين'),'<b>صوص كريمي وبروتين زيادة</b> — زبادي + ثوم + ليمون.'),
 (('juice','عصير جاهز','≈ 110 سعرة + سكر'),('fruit','فاكهة كاملة','≈ 60 سعرة + ألياف'),'<b>الألياف تشبعك</b> والعصير يرفع السكر بسرعة ويرجعك جوعانة.'),
 (('burger','برجر مطاعم','≈ 550 سعرة'),('homeburger','برجر بالبيت','≈ 380 سعرة'),'<b>لحم قليل الدهن وخبز أسمر</b> وخضار كثير — بدون صوصات جاهزة.'),
 (('pizza','بيتزا بيبروني','≈ 600 سعرة / شريحتين'),('pizza_h','بيتزا رقيقة بالخضار','≈ 350 سعرة / شريحتين'),'<b>عجينة رقيقة + جبن خفيف</b> وكثّري الخضار والدجاج.'),
 (('sweets','كيك شوكولاتة','≈ 420 سعرة'),('sweets_h','زبادي بالتوت','≈ 150 سعرة'),'<b>حلاوة طبيعية</b> — زبادي + توت + رشة شوفان أو عسل.'),
 (('chips','شيبس','≈ 270 سعرة / كيس'),('popcorn','فشار بدون زبدة','≈ 95 سعرة / ٣ أكواب'),'<b>كمية أكبر بسعرات أقل</b> — سويه بالبيت بدون زبدة ولا كراميل.'),
 (('icecream','آيسكريم','≈ 270 سعرة / كوب'),('frozen','فروزن يوغرت','≈ 200 سعرة / كوب'),'<b>فرق أصغر مما تتوقعين</b> — الأهم الكمية؛ اختاري الصغير وأضيفي فاكهة.'),
 (('white_bread','خبز أبيض','≈ 160 سعرة / شريحتين'),('brown_bread','خبز أسمر','≈ 160 سعرة / شريحتين'),'<b>السعرات تقريبًا نفسها</b> — لكن الألياف أكثر والشبع أطول.'),
 (('shawarma','شاورما مطاعم','≈ 600 سعرة'),('wrap','راب دجاج بالبيت','≈ 400 سعرة'),'<b>خبز تورتيلا أسمر</b> + دجاج مشوي + خضار + صوص زبادي بدل الثومية.'),
]
TITLES=['المقليات والدجاج','المشروبات والصوصات','العصير والبرجر','البيتزا والحلى','السناكات والآيسكريم','الخبز والشاورما']
slides=[]
# 1 غلاف
slides.append(HEAD+'''<style>.cv{position:absolute;inset:0;display:flex}.cv div{flex:1;overflow:hidden}.cv img{width:100%;height:100%;object-fit:cover}
.cv .b img{filter:saturate(.5) brightness(.6)}.shade{position:absolute;inset:0;background:linear-gradient(rgba(11,23,52,.25),rgba(11,23,52,.15) 35%,rgba(11,23,52,.96) 72%)}
.big{position:absolute;bottom:200px;right:64px;left:64px}.big h1{font-size:96px;line-height:1.15}.big h1 span{color:#1FBAEC}.big p{font-size:34px;color:#CFDCF2;margin-top:22px}
.lb{position:absolute;top:150px;font:700 28px "Readex Pro";padding:8px 22px;border-radius:40px}</style>
<div class="cv"><div class="b"><img src="img/fries.jpg"></div><div class="g"><img src="img/baked.jpg"></div></div><div class="shade"></div>
<span class="lb" style="right:64px;background:#E5484D">قبل</span><span class="lb" style="left:64px;background:#1FBAEC;color:#0B1734">بعد</span>
'''+top(1)+'''<div class="big"><h1>كلي اللي تحبينه<br><span>بنسخة صحية</span></h1><p>١٢ بديل ذكي بنفس الطعم — وبسعرات أقل بكثير</p></div>'''+FOOT+'</body></html>')
# 2..7
for i in range(6):
    a,b=SW[2*i],SW[2*i+1]
    slides.append(HEAD+top(i+2)+f'<div class="ttl"><span>بدّلي</span> {TITLES[i]}</div>'+row(236,a[:2])+why(650,a[2])+row(740,b[:2])+why(1154,b[2])+FOOT+'</body></html>')
# 8 قواعد + دعوة
slides.append(HEAD+'''<style>.rules{position:absolute;top:270px;right:64px;left:64px;display:grid;gap:34px}
.r{display:flex;gap:28px;align-items:center;background:#132650;border-radius:30px;padding:40px 36px}
.r .n{flex:none;width:84px;height:84px;border-radius:50%;background:#1FBAEC;color:#0B1734;display:grid;place-items:center;font-size:40px;font-weight:700}
.r h2{font-size:36px}.r p{font-size:27px;color:#BFD0EE;margin-top:6px}
.cta{position:absolute;bottom:110px;right:64px;left:64px;background:#fff;color:#16244A;border-radius:34px;padding:38px 40px;text-align:center}
.cta h2{font-size:42px;color:#284DA0}.cta p{font-size:29px;margin-top:10px}</style>'''+top(8)+
'''<div class="ttl">٣ قواعد <span>تمشي معك في أي أكلة</span></div><div class="rules">
<div class="r"><div class="n">١</div><div><h2>اشوي، احمّري بالفرن، أو بالقلاية الهوائية</h2><p>بدل القلي العميق — توفرين مئات السعرات</p></div></div>
<div class="r"><div class="n">٢</div><div><h2>ابدئي بالبروتين والخضار</h2><p>نص الصحن خضار، ربعه بروتين — الشبع يجي أسرع</p></div></div>
<div class="r"><div class="n">٣</div><div><h2>انتبهي للمشروب والصوص</h2><p>سعرات مخفية ما تحسين فيها</p></div></div></div>
<div class="cta"><h2>احفظي البوست وجربي بديل واحد هالأسبوع</h2><p>تبغين خطة أكل تناسبك؟ <b>navcoaching.com</b></p></div>
<div class="foot"><span>الأرقام تقريبية وتختلف حسب الحصة والمكونات</span><span></span></div></body></html>''')
for i,h in enumerate(slides,1): open(f'carousel2-{i}.html','w').write(h)
print(len(slides))
