# يرسم ثلاث لوحات SVG لأنواع الانقباض العضلي (ذراع + عضلة ذات الرأسين + دمبل)
import math, sys, os
out = sys.argv[1]
INK = "#16244a"; BRAND = "#284da0"; ACC = "#1fbaec"; ACC_SOFT = "#cfeffb"; RULE = "#b8c2d6"; PAPER = "#f2f5fa"
SX, SY = 128, 30          # الكتف
EX, EY = 128, 122         # المرفق
L = 70                   # طول الساعد

def end(a):  # a بالدرجات فوق الأفق، الساعد يتجه يسارًا (أمام الجسم)
    r = math.radians(a); return EX - L*math.cos(r), EY - L*math.sin(r)

def forearm(a, ghost=False):
    x, y = end(a)
    op = ' opacity=".28" stroke-dasharray="3 3"' if ghost else ''
    s = f'<g{op}>'
    s += f'<line x1="{EX}" y1="{EY}" x2="{x:.1f}" y2="{y:.1f}" stroke="{INK}" stroke-width="17" stroke-linecap="round"/>'
    s += f'<line x1="{EX}" y1="{EY}" x2="{x:.1f}" y2="{y:.1f}" stroke="{PAPER}" stroke-width="14.6" stroke-linecap="round"/>'
    # دمبل عمودي على الساعد
    s += f'<g transform="translate({x:.1f} {y:.1f}) rotate({-a:.1f})">'
    s += f'<rect x="-4" y="-21" width="8" height="42" rx="2" fill="{INK}"/>'
    s += f'<rect x="-9" y="-30" width="18" height="11" rx="2.5" fill="{INK}"/><rect x="-9" y="19" width="18" height="11" rx="2.5" fill="{INK}"/>'
    s += '</g></g>'
    return s

def biceps(thick, length):
    # بطن العضلة على الجهة الأمامية (اليسار) من العضد
    top, bot = SY + (94 - length)/2 + 6, EY - 8 - (94 - length)/2
    mid = (top + bot)/2; x0 = SX - 11
    return (f'<path d="M{x0} {top} C{x0-thick} {mid-length*0.32} {x0-thick} {mid+length*0.32} {x0} {bot} Z" '
            f'fill="{ACC_SOFT}" stroke="{ACC}" stroke-width="2"/>'
            f'<path d="M{x0-thick*0.45} {mid-length*0.18} Q{x0-thick*0.62} {mid} {x0-thick*0.45} {mid+length*0.18}" fill="none" stroke="{ACC}" stroke-width="1" opacity=".7"/>')

def arm():
    return (f'<line x1="{SX}" y1="{SY}" x2="{EX}" y2="{EY}" stroke="{INK}" stroke-width="24" stroke-linecap="round"/>'
            f'<line x1="{SX}" y1="{SY}" x2="{EX}" y2="{EY}" stroke="{PAPER}" stroke-width="21.6" stroke-linecap="round"/>'
            f'<circle cx="{SX}" cy="{SY}" r="13" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>'
            f'<circle cx="{EX}" cy="{EY}" r="4" fill="{INK}"/>')

def arc(a1, a2, r=88):
    p1 = (EX - r*math.cos(math.radians(a1)), EY - r*math.sin(math.radians(a1)))
    p2 = (EX - r*math.cos(math.radians(a2)), EY - r*math.sin(math.radians(a2)))
    sweep = 1 if a2 > a1 else 0
    return (f'<path d="M{p1[0]:.1f} {p1[1]:.1f} A{r} {r} 0 0 {sweep} {p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="{BRAND}" stroke-width="2" marker-end="url(#ah)"/>')

def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 190" width="400" height="380">'
            f'<defs><marker id="ah" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
            f'<path d="M0 0L10 5L0 10z" fill="{BRAND}"/></marker></defs>'
            f'<rect width="200" height="190" fill="{PAPER}"/>'
            f'<line x1="20" y1="176" x2="180" y2="176" stroke="{RULE}" stroke-width=".8"/>' + body + '</svg>')

panels = {
 'concentric': forearm(-30, True) + arm() + biceps(24, 62) + forearm(42) + arc(-18, 34),
 'eccentric':  forearm(42, True) + arm() + biceps(11, 84) + forearm(-30) + arc(34, -18),
 'isometric':  arm() + biceps(17, 72) + forearm(0) +
               f'<g fill="{BRAND}"><rect x="52" y="50" width="3.6" height="18" rx="1"/><rect x="59.5" y="50" width="3.6" height="18" rx="1"/></g>',
}
for k, b in panels.items():
    open(os.path.join(out, f'muscle-{k}.svg'), 'w').write(svg(b))
print('ok')
