/* ============================================================================
   VAGLO — site behaviour. No dependencies.
   ========================================================================== */
(function () {
  'use strict';

  /* ---------- sticky nav hairline ---------- */
  var nav = document.getElementById('nav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('stuck', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- reveal on scroll ---------- */
  var revealables = document.querySelectorAll('.rv');
  function revealAll() { revealables.forEach(function (el) { el.classList.add('in'); }); }

  if ('IntersectionObserver' in window && revealables.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.01 });
    revealables.forEach(function (el) { io.observe(el); });
    // Safety net: nothing on a marketing page may ever stay invisible.
    window.addEventListener('load', function () { setTimeout(revealAll, 2500); });
  } else {
    revealAll();
  }


  /* ---------- demo overlay ---------- */
  var veil = document.getElementById('demoVeil');
  var startBtn = document.getElementById('demoStart');
  if (veil && startBtn) {
    startBtn.addEventListener('click', function () { veil.classList.add('gone'); });
  }

  /* ---------- guided tour of the demo dashboard ---------- */
  // Each step teaches what the product does, not just where a control is.
  var TOUR = [
    { view: 'pipeline', sel: '.mock-board',
      title: 'Every pursuit, in one place',
      body: 'Opportunities move left to right, Analyzed through Accepted. Nothing sits in an inbox waiting for somebody to notice it.' },
    { view: 'pipeline', sel: '.mock-card .mc-fit',
      title: 'The fit score',
      body: 'Each one is read against your own project history and scored out of a hundred. High means it is worth your week. Middling means read it before you commit one.' },
    { view: 'pipeline', sel: '.mock-card .mc-hr',
      title: 'What it will cost you',
      body: 'An estimate of the hours the package will take, so you can weigh the effort against the fee before you say yes.' },
    { view: 'pipeline', sel: '.mock-card .mc-pf',
      title: 'Whether it is safe to send',
      body: 'Ready means every required field is filled. Not Ready means something is missing, and the package stays shut until a person resolves it.' },
    { view: 'documents', sel: '.mock-view[data-view="documents"] .mock-table',
      title: 'Drop anything in',
      body: 'Files get sorted by what is inside them rather than by their filename, then routed. An amendment that moves a deadline is caught here.' },
    { view: 'personnel', sel: '.mock-view[data-view="personnel"] .mock-table',
      title: 'Your firm, written down',
      body: 'Who holds which registration, licensed in which states, and what they have actually worked on. This is what makes staffing a pursuit arithmetic instead of memory.' },
    { view: 'scoring', sel: '.mock-view[data-view="scoring"] .mock-rules',
      title: 'It learns your taste',
      body: 'Rules you write yourself, alongside rules it worked out from your own accept and decline history. Every score shows which of them moved it.' }
  ];

  var replayBtn = document.getElementById('tourReplay');
  var tourBtn = document.getElementById('demoTour');
  var ring = null, pop = null, at = 0, live = false;

  function scrollTop() {
    return window.scrollY || document.scrollingElement.scrollTop || document.body.scrollTop || 0;
  }
  function scrollLeft() {
    return window.scrollX || document.scrollingElement.scrollLeft || document.body.scrollLeft || 0;
  }
  function scrollTo(y) {
    var el = document.scrollingElement || document.documentElement;
    if (el.scrollTo) el.scrollTo({ top: y, behavior: prefersReduced() ? 'auto' : 'smooth' });
    else el.scrollTop = y;
  }

  function place(el) {
    var r = el.getBoundingClientRect();
    var pad = 6;
    var top = r.top + scrollTop() - pad, left = r.left + scrollLeft() - pad;
    ring.style.top = top + 'px'; ring.style.left = left + 'px';
    ring.style.width = (r.width + pad * 2) + 'px'; ring.style.height = (r.height + pad * 2) + 'px';

    // If the target could not be brought on screen, a spotlight whose hole is off
    // screen just dims the page for no reason. Drop the dimming instead.
    var offscreen = r.bottom < 0 || r.top > window.innerHeight;
    ring.style.opacity = offscreen ? '0' : '1';

    // prefer below the target; flip above when it would leave the viewport
    var pw = pop.offsetWidth, ph = pop.offsetHeight;
    var below = r.bottom + 14, above = r.top - ph - 14;
    var y = (below + ph < window.innerHeight || above < 8) ? below : above;
    var x = Math.min(Math.max(r.left + r.width / 2 - pw / 2, 12), window.innerWidth - pw - 12);
    pop.style.top = (y + scrollTop()) + 'px';
    pop.style.left = (x + scrollLeft()) + 'px';
  }

  function render() {
    var step = TOUR[at];
    var nav = mockRootEl && mockRootEl.querySelector('.mock-navitem[data-view="' + step.view + '"]');
    if (nav && !nav.classList.contains('on')) nav.click();

    var target = document.querySelector(step.sel);
    if (!target) { at + 1 < TOUR.length ? (at++, render()) : end(); return; }

    pop.innerHTML = '';
    var h = document.createElement('h4'); h.textContent = step.title;
    var b = document.createElement('p'); b.textContent = step.body;
    var foot = document.createElement('div'); foot.className = 'tour-foot';
    var count = document.createElement('span'); count.className = 'tour-step';
    count.textContent = (at + 1) + ' of ' + TOUR.length;
    var skip = document.createElement('button'); skip.type = 'button'; skip.className = 'tour-skip';
    skip.textContent = 'Skip'; skip.addEventListener('click', end);
    foot.appendChild(count); foot.appendChild(skip);
    if (at > 0) {
      var back = document.createElement('button'); back.type = 'button'; back.className = 'tour-btn';
      back.textContent = 'Back'; back.addEventListener('click', function () { at--; render(); });
      foot.appendChild(back);
    }
    var next = document.createElement('button'); next.type = 'button'; next.className = 'tour-btn primary';
    next.textContent = at === TOUR.length - 1 ? 'Done' : 'Next';
    next.addEventListener('click', function () {
      if (at === TOUR.length - 1) { end(); return; }
      at++; render();
    });
    foot.appendChild(next);
    pop.appendChild(h); pop.appendChild(b); pop.appendChild(foot);

    var r = target.getBoundingClientRect();
    if (r.top < 70 || r.bottom > window.innerHeight - 20) {
      // scrollIntoView handles nested scroll containers, which a manual
      // scrollTo on the document does not
      try {
        target.scrollIntoView({ block: 'center', inline: 'nearest',
                                behavior: prefersReduced() ? 'auto' : 'smooth' });
      } catch (e) { target.scrollIntoView(false); }
      setTimeout(function () { place(target); }, prefersReduced() ? 0 : 400);
    }
    place(target);
    next.focus();
  }

  function prefersReduced() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function start() {
    if (live || !mockRootEl) return;
    // Ask whether the dashboard is actually on screen rather than inferring it from
    // viewport width -- a hidden or zero-width pane reports as mobile and would
    // otherwise silently refuse to start.
    if (getComputedStyle(mockRootEl).display === 'none') return;
    live = true; at = 0;
    if (veil) veil.classList.add('gone');
    ring = document.createElement('div'); ring.className = 'tour-ring';
    pop = document.createElement('div'); pop.className = 'tour-pop';
    pop.setAttribute('role', 'dialog'); pop.setAttribute('aria-label', 'Dashboard tour');
    document.body.appendChild(ring); document.body.appendChild(pop);
    document.addEventListener('keydown', onKey);
    window.addEventListener('resize', onResize);
    window.addEventListener('scroll', onResize, { passive: true });
    document.addEventListener('scroll', onResize, { passive: true, capture: true });
    if (replayBtn) replayBtn.hidden = true;
    var frame = mockRootEl.closest('.frame');
    if (frame) {
      var fr = frame.getBoundingClientRect();
      if (fr.top < 0 || fr.top > window.innerHeight * 0.4) {
        try { frame.scrollIntoView({ block: 'start', behavior: prefersReduced() ? 'auto' : 'smooth' }); }
        catch (e) { frame.scrollIntoView(); }
      }
    }
    setTimeout(render, prefersReduced() ? 0 : 420);
  }

  function end() {
    live = false;
    document.removeEventListener('keydown', onKey);
    window.removeEventListener('resize', onResize);
    window.removeEventListener('scroll', onResize);
    document.removeEventListener('scroll', onResize, true);
    if (ring) { ring.remove(); ring = null; }
    if (pop) { pop.remove(); pop = null; }
    if (replayBtn) replayBtn.hidden = false;
  }

  function onKey(e) {
    if (e.key === 'Escape') end();
    else if (e.key === 'ArrowRight' && at < TOUR.length - 1) { at++; render(); }
    else if (e.key === 'ArrowLeft' && at > 0) { at--; render(); }
  }
  function onResize() {
    if (!live) return;
    var t = document.querySelector(TOUR[at].sel);
    if (t) place(t);
  }

  var mockRootEl = document.getElementById('mock');
  if (tourBtn) tourBtn.addEventListener('click', start);
  if (replayBtn) replayBtn.addEventListener('click', start);

  /* ---------- mock dashboard: view switching + drag/drop ---------- */
  var mockRoot = document.getElementById('mock');
  if (mockRoot) {
    var titles = {
      pipeline: 'RFP Pipeline', proposals: 'Proposals', documents: 'Document Intake',
      projects: 'Projects', personnel: 'Personnel', subs: 'Subconsultants',
      metrics: 'Metrics', scoring: 'Scoring Rules'
    };
    var titleEl = document.getElementById('mockTitle');

    mockRoot.querySelectorAll('.mock-navitem').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var v = btn.dataset.view;
        mockRoot.querySelectorAll('.mock-navitem').forEach(function (o) { o.classList.remove('on'); });
        btn.classList.add('on');
        mockRoot.querySelectorAll('.mock-view').forEach(function (o) { o.classList.toggle('on', o.dataset.view === v); });
        if (titleEl) titleEl.textContent = titles[v] || v;
      });
    });

    // Same transition map the real board enforces.
    var VALID = {
      analysis: ['declined', 'proposal'],
      declined: [],
      proposal: ['declined', 'submitted'],
      submitted: ['rejected', 'accepted'],
      rejected: [], accepted: []
    };
    var dragged = null;

    function recount() {
      mockRoot.querySelectorAll('.mock-col').forEach(function (col) {
        var n = col.querySelectorAll('.mock-card').length;
        var em = col.querySelector('.mock-colhead em');
        if (em) em.textContent = n;
        var drop = col.querySelector('.mock-drop');
        var empty = drop.querySelector('.mock-empty');
        if (n === 0 && !empty) {
          var d = document.createElement('div'); d.className = 'mock-empty'; d.textContent = 'No items'; drop.appendChild(d);
        } else if (n > 0 && empty) { empty.remove(); }
      });
    }

    mockRoot.querySelectorAll('.mock-card').forEach(function (card) {
      card.addEventListener('dragstart', function (e) {
        dragged = card; card.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        try { e.dataTransfer.setData('text/plain', 'card'); } catch (err) {}
      });
      card.addEventListener('dragend', function () {
        card.classList.remove('dragging'); dragged = null;
        mockRoot.querySelectorAll('.mock-drop').forEach(function (d) { d.classList.remove('ok', 'no'); });
      });
    });

    mockRoot.querySelectorAll('.mock-col').forEach(function (col) {
      var drop = col.querySelector('.mock-drop');
      var target = col.dataset.stage;

      col.addEventListener('dragover', function (e) {
        if (!dragged) return;
        var from = dragged.dataset.stage;
        var allowed = from !== target && (VALID[from] || []).indexOf(target) !== -1;
        drop.classList.toggle('ok', allowed);
        drop.classList.toggle('no', !allowed && from !== target);
        if (allowed) { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; }
      });
      col.addEventListener('dragleave', function () { drop.classList.remove('ok', 'no'); });
      col.addEventListener('drop', function (e) {
        e.preventDefault();
        drop.classList.remove('ok', 'no');
        if (!dragged) return;
        var from = dragged.dataset.stage;
        if ((VALID[from] || []).indexOf(target) === -1) return;
        dragged.dataset.stage = target;
        drop.appendChild(dragged);
        recount();
      });
    });
  }

  /* ---------- contact form ---------- */
  var form = document.getElementById('callform');
  if (form) {
    form.addEventListener('submit', function (e) {
      // No endpoint wired yet: compose a mail draft so nothing is ever lost.
      if (form.dataset.endpoint) return; // real endpoint present -- let it post
      e.preventDefault();
      var d = new FormData(form);
      var lines = [];
      d.forEach(function (v, k) {
        if (String(v).trim() === '') return;
        lines.push(k.replace(/_/g, ' ').toUpperCase() + ':\n' + v + '\n');
      });
      var to = form.dataset.email || 'hello@vaglo.example';
      var subject = 'Discovery call request - ' + (d.get('firm') || 'new enquiry');
      window.location.href = 'mailto:' + to +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(lines.join('\n'));
      var ok = document.getElementById('formok');
      if (ok) ok.hidden = false;
    });
  }
})();

/* ============================================================================
   Assistant. Answers from a curated knowledge base, matched on keywords.
   No backend and no API key, so it is honest about what it does not know and
   hands those questions to a person instead of inventing an answer.
   ========================================================================== */
(function () {
  'use strict';
  var fab = document.getElementById('chatFab');
  var panel = document.getElementById('chatPanel');
  if (!fab || !panel) return;

  var log = document.getElementById('chatLog');
  var form = document.getElementById('chatForm');
  var text = document.getElementById('chatText');
  var chips = document.getElementById('chatChips');
  var closeBtn = document.getElementById('chatClose');

  var KB = [
    { k: ['cost','price','pricing','how much','expensive','budget','quote','afford'],
      a: 'Two parts. A one-time setup that scales with how much history has to be loaded into the database, and a flat monthly covering the nightly watch, updates and a set number of support hours. The setup is the half that varies, because a firm with twenty projects is not the same job as one with two hundred. <a href="pricing.html">How pricing works</a> explains it, and you get your actual number in writing after the call, before you commit to anything.' },
    { k: ['data','cloud','secure','security','privacy','server','on-prem','premise','where does'],
      a: 'In a private instance built for your firm alone, never pooled with another client. Your opportunities, decisions and pricing posture are never used for anyone else’s pursuits, and the AI services that read your documents do not train on them. Full export whenever you ask, and certified deletion within thirty days if you leave.' },
    { k: ['make things up','hallucinat','invent','made up','accurate','trust','wrong','fabricat'],
      a: 'It is built not to. Anything it cannot source becomes a visible blank, and it blocks the package until a person fills it in. Facts your records own get written back over anything it generated. The trade is that a thin database gives you a package with visible gaps, which is why the archive work at the start is not optional.' },
    { k: ['setup','set up','how long','time','onboard','implement','start','install'],
      a: 'The reading and extracting is machine work, so you are not retyping anything. Your time goes into answering the questions only your firm can answer. Real hours, but a few sessions rather than a months-long project.' },
    { k: ['fit','right for','suitable','good for','work for us','my firm','small'],
      a: 'Best fit is engineering, architecture and construction management firms that already win federal work and want to chase more of it. Probably not a fit if you bid commercial RFPs, or if you do not have a project history to load yet. Tell me what you bid on and I will give you a straight answer.' },
    { k: ['produce','output','deliver','generate','make','package','document','sf330','form','section'],
      a: 'The whole submittable package. A resume for each person in each role, past-performance project sheets, the org chart, the participation matrix, the narrative, and a qualifications form for every teaming partner. Then it merges the lot with a cover, contents, tab dividers and page numbers. One real package on record ran 61 pages.' },
    { k: ['night','overnight','sam','find','discover','opportunit','solicitation','notice','brief'],
      a: 'Every night it reads the federal notices that were posted, downloads the whole package including attachments, re-checks anything you are already tracking for amendments or withdrawals, and emails you a short brief. Each one gets a fit score with the reasoning next to it.' },
    { k: ['review','check','quality','red team','preflight','compliance','mistake'],
      a: 'Four passes before you send. A preflight on completeness, page limits, expired licences and unacknowledged amendments. A consistency audit across sections. A red team that scores it the way a government evaluation board would. And a check that every scored criterion was actually answered. On one live package that last check caught a Quality Control factor the draft never addressed.' },
    { k: ['learn','score','fit score','decision','go/no-go','no bid','bid decision','rules'],
      a: 'Three layers. An AI read of the solicitation, plain-English rules you write yourself, and a statistical model trained on your own accept and decline history. Hover any score and it shows which rule fired and by how much. The learned layer sits at zero weight until enough decisions exist, so it cannot learn the wrong thing from your first ten calls.' },
    { k: ['who','you','founder','team','company','behind','support'],
      a: 'A small shop, and you will be talking to the person who builds it. The system was built for a working federal engineering firm and used on live pursuits for months before it was offered to anyone else.' },
    { k: ['windows','mac','linux','platform','install','software','maintain'],
      a: 'Nothing to install and nothing to maintain: we host it, sweep SAM.gov every morning and keep it current. Whatever your office runs on makes no difference. One person on your team learns the dashboard, and we train them; they assemble the package there when you decide to pursue.' },
    { k: ['cm','construction management','civil','structural','environmental','discipline','not engineering'],
      a: 'The discovery and analysis half transfers to construction management and adjacent disciplines. What changes is the vocabulary and the deliverable format, which is authoring work rather than a rewrite. It produces the federal qualifications package specifically, so it does not write general commercial RFP responses.' },
    { k: ['contract','cancel','stop','lock','leave','own'],
      a: 'The database we build is yours. Full export of everything, documents included, whenever you ask, and certified deletion within thirty days if you leave. The longer it runs the more your own history is worth, and that asset belongs to you.' },
    { k: ['demo','see it','show me','try','walkthrough'],
      a: (matchMedia('(max-width: 620px)').matches
        ? 'There is a live dashboard on this page, but it needs a full screen, so it is hidden on phones. Open the page on a laptop and you can work every tab of it.'
        : 'The dashboard on this page is live, so click around it.')
        + ' For the real thing on your own work, that is what the call is for. <a href="contact.html">Request one here</a>.' }
  ];

  var FALLBACK = 'I do not have a good answer to that one, and I would rather not guess. <a href="contact.html">Send it to me directly</a> and you will get a real answer.';

  function bubble(cls, html) {
    var d = document.createElement('div');
    d.className = 'chat-msg ' + cls;
    d.innerHTML = html;
    log.appendChild(d);
    log.scrollTop = log.scrollHeight;
    return d;
  }

  function answer(q) {
    var s = q.toLowerCase(), best = null, bestScore = 0;
    KB.forEach(function (item) {
      var score = 0;
      item.k.forEach(function (kw) { if (s.indexOf(kw) !== -1) score += kw.length; });
      if (score > bestScore) { bestScore = score; best = item; }
    });
    return best ? best.a : FALLBACK;
  }

  function ask(q) {
    if (!q.trim()) return;
    bubble('you', q.replace(/</g, '&lt;'));
    if (chips) chips.style.display = 'none';
    var t = bubble('bot', '<span class="chat-typing"><span></span><span></span><span></span></span>');
    setTimeout(function () {
      t.innerHTML = answer(q);
      log.scrollTop = log.scrollHeight;
    }, 420 + Math.random() * 260);
  }

  function toggle(open) {
    panel.classList.toggle('open', open);
    fab.classList.toggle('open', open);
    fab.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) setTimeout(function () { text.focus(); }, 220);
  }

  fab.addEventListener('click', function () { toggle(!panel.classList.contains('open')); });
  if (closeBtn) closeBtn.addEventListener('click', function () { toggle(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') toggle(false); });

  if (chips) {
    chips.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () { ask(b.textContent); });
    });
  }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    ask(text.value);
    text.value = '';
  });
})();
