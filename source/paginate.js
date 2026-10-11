// يوزّع محتوى كل فصل (section.flow) على صفحات A4 تلقائيًا، ويضيف الترويسة والتذييل وأرقام الصفحات والفهرس.
(async function () {
  await document.fonts.ready;
  const book = document.getElementById('book');
  const src = document.getElementById('src');
  const LOGO = 'img/logo-color.png';

  function chrome(page, num, title) {
    const ph = document.createElement('header');
    ph.className = 'ph';
    ph.innerHTML = (num ? `<span class="ph-num">${num}</span>` : '') +
      `<span class="ph-title">${title}</span><span class="ph-line"></span><img src="${LOGO}" alt="Nav Coaching">`;
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
  // يقسم جدولًا أو قائمة على أكثر من صفحة
  function splitInto(el, pc, sec) {
    const isTable = el.tagName === 'TABLE';
    const items = isTable ? [...el.tBodies[0].rows] : [...el.children];
    let shell = el.cloneNode(false);
    if (isTable) { if (el.tHead) shell.appendChild(el.tHead.cloneNode(true)); shell.appendChild(document.createElement('tbody')); }
    pc.appendChild(shell);
    let holder = isTable ? shell.tBodies[0] : shell;
    for (const it of items) {
      holder.appendChild(it);
      if (over(pc)) {
        holder.removeChild(it);
        if (!holder.children.length) shell.remove();
        pc = newPage(sec);
        shell = el.cloneNode(false);
        if (isTable) { if (el.tHead) shell.appendChild(el.tHead.cloneNode(true)); shell.appendChild(document.createElement('tbody')); }
        if (!isTable && el.tagName === 'OL') shell.setAttribute('start', (it.value || 0));
        pc.appendChild(shell);
        holder = isTable ? shell.tBodies[0] : shell;
        holder.appendChild(it);
      }
    }
    return pc;
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
      // نقل العناوين المعلّقة مع ما بعدها
      const carry = [];
      while (pc.lastElementChild && isKeep(pc.lastElementChild)) carry.unshift(pc.removeChild(pc.lastElementChild));
      if (splittable(el) && !carry.length) { pc = splitInto(el, pc, sec); continue; }
      if (pc.children.length) pc = newPage(sec);
      carry.forEach((c) => pc.appendChild(c));
      if (splittable(el)) { pc = splitInto(el, pc, sec); continue; }
      pc.appendChild(el);
      if (over(pc)) console.warn('OVERFLOW block', sec.dataset.title, el.outerHTML.slice(0, 80));
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

  // فحص التجاوز
  const issues = [];
  pages.forEach((p, i) => {
    const pc = p.querySelector('.pc');
    if (pc && over(pc)) issues.push(i + 1);
    p.querySelectorAll('img').forEach((im) => { if (!im.complete || !im.naturalWidth) issues.push('img:' + (i + 1)); });
  });
  window.__layout = { pages: pages.length, issues };
  document.body.dataset.ready = '1';
})();
