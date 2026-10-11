// يوزّع محتوى كل فصل (section.flow) على صفحات A4 تلقائيًا، ويضيف الترويسة والتذييل وأرقام الصفحات والفهرس.
(async function () {
  // نسخة الجوال: book.html?m=1 — صفحة أصغر ونص أكبر نسبيًا
  if (/[?&]m=1/.test(location.search)) {
    document.documentElement.classList.add('m');
    const st = document.createElement('style');
    st.textContent = '@page{size:115mm 204mm;margin:0}';
    document.head.appendChild(st);
  }
  // تحميل كل الخطوط قبل القياس (المحتوى المخفي لا يطلبها تلقائيًا)
  await Promise.all([...document.fonts].map((f) => f.load().catch(() => 0)));
  await document.fonts.ready;
  const book = document.getElementById('book');
  const src = document.getElementById('src');
  const LOGO = 'img/logo-color.png';

  // ترقيم المفاهيم الخاطئة قبل التوزيع
  src.querySelectorAll('.myth').forEach((m, i) => { m.dataset.n = String(i + 1).padStart(2, '0'); });
  // عناوين كل فصل لقائمة «في هذا الفصل» في صفحة الافتتاح
  const chapterHeads = {};
  src.querySelectorAll('section.flow[data-num]').forEach((sec) => {
    chapterHeads[sec.dataset.num] = [...sec.querySelectorAll(':scope > h2')].map((h, i) => {
      if (!h.id) h.id = `c${sec.dataset.num}-${i + 1}`;
      return h;
    });
  });

  function chrome(page, num, title) {
    const ph = document.createElement('header');
    ph.className = 'ph';
    ph.innerHTML = (num ? `<span class="ph-num">${num}</span>` : '') +
      `<span class="ph-title">${title}</span><span class="ph-line"></span><a class="ph-logo" href="#toc" title="الفهرس"><img src="${LOGO}" alt="Nav Coaching — العودة إلى الفهرس"></a>`;
    page.appendChild(ph);
  }
  function footer(page) {
    const pf = document.createElement('footer');
    pf.className = 'pf';
    pf.innerHTML = '<span class="pnum"></span><span class="site">navcoaching.com</span>';
    page.appendChild(pf);
  }
  function newPage(sec) {
    const page = document.createElement('div');
    page.className = 'page content-page ' + (sec.dataset.cls || '');
    if (sec.dataset.title) chrome(page, sec.dataset.num, sec.dataset.title);
    const pc = document.createElement('main');
    pc.className = 'pc';
    page.appendChild(pc);
    footer(page);
    book.appendChild(page);
    return pc;
  }
  const over = (pc) => pc.scrollHeight > pc.clientHeight + 1;
  const isKeep = (el) => el && /^H[23]$/.test(el.tagName) || (el && el.classList && el.classList.contains('kwn'));

  function splittable(el) {
    return el.matches && (el.matches('table.split') || el.matches('ul.split,ol.split'));
  }
  // يقسم جدولًا أو قائمة أو أي حاوية متعددة العناصر على أكثر من صفحة
  function splitInto(el, pc, sec) {
    const isTable = el.tagName === 'TABLE';
    const raw = isTable ? [...el.tBodies[0].rows] : [...el.children];
    // إبقاء المصطلح مع شرحه في قوائم التعريف
    const groups = [];
    raw.forEach((it) => {
      if (it.tagName === 'DD' && groups.length && groups[groups.length - 1][0].tagName === 'DT') groups[groups.length - 1].push(it);
      else groups.push([it]);
    });
    const isSteps = el.matches('ol.steps');
    let placed = 0;
    const makeShell = () => {
      const sh = el.cloneNode(false);
      if (isTable) { if (el.tHead) sh.appendChild(el.tHead.cloneNode(true)); sh.appendChild(document.createElement('tbody')); }
      if (isSteps) sh.style.counterReset = `s ${placed}`;
      return sh;
    };
    let shell = makeShell();
    pc.appendChild(shell);
    let holder = isTable ? shell.tBodies[0] : shell;
    for (const g of groups) {
      g.forEach((it) => holder.appendChild(it));
      if (over(pc) && holder.children.length > g.length) {
        g.forEach((it) => holder.removeChild(it));
        pc = newPage(sec);
        shell = makeShell();
        pc.appendChild(shell);
        holder = isTable ? shell.tBodies[0] : shell;
        g.forEach((it) => holder.appendChild(it));
      }
      else if (over(pc) && pc.children.length > 1) {
        // حتى الصف الأول لا يتسع: انقل الجدول كله إلى صفحة جديدة
        pc.removeChild(shell);
        pc = newPage(sec);
        pc.appendChild(shell);
      }
      if (isSteps) placed += g.filter((x) => x.tagName === 'LI').length;
    }
    return pc;
  }

  // يقسم فقرة نصية بين صفحتين لملء المساحة المتبقية
  function fillParagraph(el, pc) {
    const head = el.cloneNode(false);
    head.classList.add('p-cont');
    pc.appendChild(head);
    while (el.firstChild) {
      const n = el.firstChild;
      head.appendChild(n);
      if (!over(pc)) continue;
      head.removeChild(n);
      if (n.nodeType === 3) {
        const words = n.textContent.split(/(\s+)/);
        let lo = 0, hi = words.length;
        const probe = document.createTextNode('');
        head.appendChild(probe);
        while (lo < hi) { const mid = (lo + hi + 1) >> 1; probe.textContent = words.slice(0, mid).join(''); if (over(pc)) hi = mid - 1; else lo = mid; }
        probe.textContent = words.slice(0, lo).join('');
        n.textContent = words.slice(lo).join('').replace(/^\s+/, '');
        if (!probe.textContent.trim()) head.removeChild(probe);
      }
      el.insertBefore(n, el.firstChild);
      break;
    }
    if (!head.textContent.trim()) { pc.removeChild(head); return false; }
    return true;
  }

  for (const node of [...src.children]) {
    if (!node.classList.contains('flow')) { book.appendChild(node); continue; }
    const sec = node;
    let pc = newPage(sec);
    const blocks = [...sec.children];
    for (let i = 0; i < blocks.length; i++) {
      const el = blocks[i];
      if (el.classList.contains('pagebreak')) { if (pc.children.length) pc = newPage(sec); continue; }
      pc.appendChild(el);
      if (!over(pc)) continue;
      pc.removeChild(el);
      // فقرة طويلة ومساحة كافية: اقسمها بدل ترك فراغ
      if (el.tagName === 'P' && !el.closest('.chead')) {
        const used = pc.lastElementChild ? pc.lastElementChild.getBoundingClientRect().bottom - pc.getBoundingClientRect().top : 0;
        if (pc.clientHeight - used > 90 && fillParagraph(el, pc)) {
          pc = newPage(sec);
          i--; continue; // أعد معالجة بقية الفقرة في الصفحة الجديدة
        }
      }
      // الخلاصة تنتقل مع آخر عنصر قبلها حتى لا تبقى وحدها
      if (el.classList.contains('summary') && pc.children.length > 1 && !isKeep(pc.lastElementChild)) {
        const prev = pc.removeChild(pc.lastElementChild);
        pc = newPage(sec);
        pc.appendChild(prev);
        pc.appendChild(el);
        if (!over(pc)) continue;
        pc.removeChild(el);
      }
      // نقل العناوين المعلّقة مع ما بعدها
      const carry = [];
      while (pc.lastElementChild && isKeep(pc.lastElementChild)) carry.unshift(pc.removeChild(pc.lastElementChild));
      if (splittable(el) && !carry.length) { pc = splitInto(el, pc, sec); continue; }
      if (pc.children.length) pc = newPage(sec);
      carry.forEach((c) => pc.appendChild(c));
      if (splittable(el)) { pc = splitInto(el, pc, sec); continue; }
      pc.appendChild(el);
      if (over(pc) && el.children.length > 1 && !el.classList.contains('chead')) { pc.removeChild(el); pc = splitInto(el, pc, sec); continue; }
      if (over(pc)) console.warn('OVERFLOW', book.children.length, sec.dataset.title, el.outerHTML.slice(0, 60));
    }
  }
  src.remove();

  // أرقام الصفحات
  const pages = [...book.querySelectorAll('.page')];
  pages.forEach((p, i) => { const n = p.querySelector('.pnum'); if (n) n.textContent = i + 1; });

  // الفهرس
  document.querySelectorAll('[data-toc]').forEach((li) => {
    const t = document.getElementById(li.dataset.toc);
    if (!t) return;
    const pg = t.closest('.page');
    li.querySelector('.pg').textContent = pages.indexOf(pg) + 1;
  });

  // شرائط الشعار المائلة على كامل الصفحة — أشكال متجهة بألوان صلبة قريبة من لون الورق
  const PAL = {
    content: ['#ECF2FA', '#E6F3FB', '#E0E8F6'],
    dense:   ['#EFF3FA', '#ECF4FA', '#E8EDF7'],
    dark:    ['#0B1D41', '#0D2350', '#123064'],
  };
  function slashes(kind) {
    const [a, b, c] = PAL[kind];
    const dx = 138; // ميل الشعار ≈ 25° عن الرأسي على ارتفاع 297 مم
    const bar = (x, w, fill) => `<polygon points="${x + dx},0 ${x + dx + w},0 ${x + w},297 ${x},297" fill="${fill}"/>`;
    const group = (x) => bar(x, 26, a) + bar(x + 38, 26, b) + bar(x + 76, 9, c);
    return `<svg class="slashes" viewBox="0 0 210 297" preserveAspectRatio="none" aria-hidden="true">${group(-112) + group(56)}</svg>`;
  }
  pages.forEach((p) => {
    let kind = 'content';
    if (p.classList.contains('cover') || p.classList.contains('contact')) kind = 'dark';
    else if (p.querySelector('table, .days, .ws')) kind = 'dense';
    p.insertAdjacentHTML('afterbegin', slashes(kind));
  });

  // انتظار تحميل الصور قبل الفحص
  await Promise.all([...document.images].map((im) => (im.complete ? 0 : im.decode().catch(() => 0))));
  // فحص التجاوز
  const issues = [];
  pages.forEach((p, i) => {
    const pc = p.querySelector('.pc');
    if (pc && pc.scrollHeight > pc.clientHeight + 3) issues.push(i + 1);
    p.querySelectorAll('img').forEach((im) => { if (!im.complete || !im.naturalWidth) issues.push('img:' + (i + 1)); });
  });
  window.__layout = { pages: pages.length, issues };
  document.body.dataset.ready = '1';
})();
