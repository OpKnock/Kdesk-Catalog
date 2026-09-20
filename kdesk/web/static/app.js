/* Kdesk dashboard SPA — hash router + API client + pages */
"use strict";

const $ = (sel, root) => (root || document).querySelector(sel);
const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

async function api(path, opts) {
  let res;
  try {
    res = await fetch(path, Object.assign(
      { headers: { "Content-Type": "application/json" } }, opts || {}));
  } catch (e) {
    throw new Error("Cannot reach the Kdesk server — run `kdesk serve` and open http://127.0.0.1:8000 (not this file directly).");
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = (data && data.error) || ("HTTP " + res.status);
    throw new Error(msg + (res.status === 404 ? " — is your server up to date? Restart `kdesk serve`." : ""));
  }
  return data;
}

function toast(msg) {
  const t = $("#toast");
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(t._h);
  t._h = setTimeout(() => t.classList.remove("show"), 2600);
}

function openModal(html) {
  $("#modal-box").innerHTML = html;
  $("#modal").classList.add("show");
}
function closeModal() { $("#modal").classList.remove("show"); }
$("#modal").addEventListener("click", (e) => { if (e.target.id === "modal") closeModal(); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeModal(); });

function pillFor(status) {
  const s = String(status || "").toUpperCase();
  if (["OK", "PASS", "SUCCESS", "CLEAN"].includes(s)) return `<span class="pill ok">${s}</span>`;
  if (["FAIL", "ERROR", "FAILED", "BLOCKED"].includes(s)) return `<span class="pill bad">${s}</span>`;
  if (["SKIP", "PENDING", "DRY-RUN", "PARTIAL"].includes(s)) return `<span class="pill warn">${s}</span>`;
  return `<span class="pill info">${s || "—"}</span>`;
}

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"]/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

/* original line-art: orbit emblem, bone-on-transparent */
const EMPTY_ART = `<svg width="72" height="72" viewBox="0 0 64 64" fill="none" aria-hidden="true">
  <ellipse cx="32" cy="34" rx="26" ry="10.5" transform="rotate(-18 32 34)" stroke="#8a6a1f" stroke-width="1.6"/>
  <path d="M32 10 L36.6 24.4 L51.8 24.9 L39.9 33.9 L43.8 48.4 L32 40 L20.2 48.4 L24.1 33.9 L12.2 24.9 L27.4 24.4 Z"
    stroke="#1a1917" stroke-width="1.8" stroke-linejoin="round"/></svg>`;

function emptyState(text) {
  return `<div class="empty-art">${EMPTY_ART}<p class="muted" style="font-size:13.5px">${text}</p></div>`;
}

function setBusy(btn, busy, label) {
  if (busy) {
    btn.disabled = true;
    btn.dataset.label = btn.innerHTML;
    btn.innerHTML = `<span class="spin"></span>${label || "Working…"}`;
  } else {
    btn.disabled = false;
    if (btn.dataset.label) btn.innerHTML = btn.dataset.label;
  }
}

/* thin top progress bar — always moving during loads */
let topTimer = null;
function topStart() {
  const bar = $("#topbar");
  bar.classList.add("on");
  let w = 8;
  bar.style.width = w + "%";
  clearInterval(topTimer);
  topTimer = setInterval(() => {
    w = Math.min(94, w + (100 - w) * 0.06);
    bar.style.width = w + "%";
  }, 250);
}
function topDone() {
  const bar = $("#topbar");
  clearInterval(topTimer);
  bar.style.width = "100%";
  setTimeout(() => { bar.classList.remove("on"); bar.style.width = "0"; }, 350);
}

/* ---------------- identity / onboarding ---------------- */
function userName() { return localStorage.getItem("kdesk_name") || ""; }

function bootIdentity() {
  const msgs = [
    "Universal AI agent catalog · 3,093 definitions · 45 platforms",
    "Warming up the catalog in the background…",
    "First run parses everything — next visits take seconds",
  ];
  let mi = 0;
  const sub = document.querySelector(".splash-sub");
  const rot = setInterval(() => {
    mi = (mi + 1) % msgs.length;
    if (sub && !$("#splash").classList.contains("done")) sub.textContent = msgs[mi];
    else clearInterval(rot);
  }, 2600);
  return new Promise((resolve) => {
    const done = () => {
      clearInterval(rot);
      $("#splash").classList.add("done");
      $("#app").classList.add("ready");
      paintGreet();
      resolve();
    };
    setTimeout(() => {
      if (userName()) { done(); return; }
      $("#onboard").classList.add("show");
      const input = $("#name-input");
      setTimeout(() => input.focus(), 500);
      const go = () => {
        const v = input.value.trim();
        if (!v) { input.focus(); return; }
        localStorage.setItem("kdesk_name", v);
        $("#onboard").classList.remove("show");
        toast(`Welcome, ${v}`);
        setTimeout(done, 250);
      };
      $("#name-go").onclick = go;
      input.onkeydown = (e) => { if (e.key === "Enter") go(); };
    }, 1400);
  });
}

function paintGreet() {
  const n = userName();
  const h = new Date().getHours();
  const part = h < 12 ? "morning" : h < 17 ? "afternoon" : "evening";
  $("#greet").innerHTML = n
    ? `Good ${part},<br><b>${esc(n)}</b> <span class="gear" id="gear" title="Settings">⚙</span>`
    : `Kdesk dashboard<br><b>v1.1.0</b> <span class="gear" id="gear" title="Settings">⚙</span>`;
  const g = $("#gear");
  if (g) g.onclick = openSettings;
}

function openSettings() {
  openModal(`<h2>Settings</h2>
    <p class="muted" style="margin:8px 0 14px">Your display name (stored only in this browser).</p>
    <input type="text" id="set-name" value="${esc(userName())}" maxlength="40" style="width:100%">
    <div class="row" style="margin-top:16px">
      <button id="set-save">Save</button>
      <button class="ghost" onclick="closeModal()">Cancel</button>
    </div>`);
  const inp = $("#set-name");
  setTimeout(() => { inp.focus(); inp.select(); }, 100);
  const save = () => {
    const v = inp.value.trim();
    if (!v) return;
    localStorage.setItem("kdesk_name", v);
    closeModal(); paintGreet(); toast(`Saved — welcome, ${v}`);
  };
  $("#set-save").onclick = save;
  inp.onkeydown = (e) => { if (e.key === "Enter") save(); };
}

/* ---------------- nav + router ---------------- */
const PAGES = [
  ["dashboard", "01", "Home"],
  ["catalog", "02", "Catalog"],
  ["converter", "03", "Converter"],
  ["doctor", "04", "Doctor"],
  ["marketplace", "05", "Marketplace"],
  ["install", "06", "Install"],
];

function paintNav(active) {
  $("#nav").innerHTML = PAGES.map(([id, num, label]) =>
    `<button class="nav-item${id === active ? " active" : ""}" data-page="${id}">
       <span class="num">${num}</span><span class="txt">${label}</span>
     </button>`).join("");
  $$("#nav .nav-item").forEach((b) => {
    b.onclick = () => { location.hash = "#/" + b.dataset.page; };
  });
}

const RENDER = {};

async function route() {
  const id = (location.hash || "#/dashboard").replace("#/", "") || "dashboard";
  const page = RENDER[id] ? id : "dashboard";
  paintNav(page);
  const main = $("#main");
  topStart();
  main.innerHTML = `<div class="page"><p class="muted">Loading…</p></div>`;
  try {
    main.innerHTML = `<div class="page">${await RENDER[page]()}</div><div class="colophon">Kdesk — universal agent catalog · MMXXVI</div>`;
    if (RENDER[page + "$mount"]) RENDER[page + "$mount"]();
  } catch (e) {
    main.innerHTML = `<div class="page"><h1>Something broke</h1>
      <p class="lede">${esc(e.message)}</p>
      <button class="ghost" onclick="location.reload()">Retry</button></div>`;
  } finally {
    topDone();
  }
  $("#main").scrollTop = 0;
}
window.addEventListener("hashchange", route);

/* ---------------- dashboard ---------------- */
RENDER.dashboard = async () => {
  let stats = null, tele = null, plats = [];
  try { stats = await api("/api/stats?fast=true"); } catch (e) { /* hero renders anyway */ }
  try { tele = await api("/api/telemetry"); } catch (e) { /* optional */ }
  try { plats = await api("/api/platforms"); } catch (e) { /* optional */ }
  const n = userName();
  const nagents = stats ? (stats.agents ?? "1,858") : "1,858";
  const nskills = stats ? (stats.skills ?? "1,235") : "1,235";
  const platsN = plats.length ? String(plats.length) : (stats ? String(stats.platforms ?? "45") : "45");
  const teleLine = tele && tele.total ? ` · ${tele.total} tracked runs` : "";
  const mq = plats.length
    ? plats.map((p) => `<span class="mq-item">${esc(p.id)}</span>`).join("")
    : "";
  const feats = [
    ["catalog", "02", "Catalog", "Browse every agent & skill by category."],
    ["converter", "03", "Converter", "Ship to 45 platforms — or convert your own files."],
    ["doctor", "04", "Doctor", "Scan any project, see the proof, fix with confidence."],
    ["marketplace", "05", "Marketplace", "Publish, resolve and version skills."],
    ["install", "06", "Install", "Dry-run installs, drift checks, rollbacks."],
  ];
  return `
  <div class="hero">
    <div class="hero-grid-bg"></div>
    <svg class="hero-art" viewBox="0 0 200 200" fill="none" aria-hidden="true">
      <circle cx="100" cy="100" r="86" stroke="#8a6a1f" stroke-width="1" opacity="0.5"/>
      <circle cx="100" cy="100" r="64" stroke="#8a6a1f" stroke-width="1" opacity="0.35" stroke-dasharray="3 6"/>
      <ellipse cx="100" cy="100" rx="92" ry="34" transform="rotate(-18 100 100)" stroke="#8a6a1f" stroke-width="1.2" opacity="0.6"/>
      <path d="M100 62 L109 89 L137 90 L114 106 L121 133 L100 118 L79 133 L86 106 L63 90 L91 89 Z"
        stroke="#1a1917" stroke-width="2" stroke-linejoin="round" fill="rgba(138,106,31,0.08)"/>
      <circle cx="100" cy="100" r="3.5" fill="#8a6a1f"/>
      <path d="M100 6v10M100 184v10M6 100h10M184 100h10" stroke="#8a6a1f" stroke-width="1.2" opacity="0.6"/>
    </svg>
    <div class="hero-inner">
      <div class="hero-kicker"><span class="dot"></span>Universal agent catalog · Est. MMXXVI</div>
      <div class="hero-title">Every agent.<br><em>Every platform.</em></div>
      <p class="hero-sub">${n ? esc(n) + " — pick" : "Pick"} any of ${nagents} agents &amp; ${nskills} skills, ship to ${platsN} platforms, diagnose any project — all from this room${teleLine}.</p>
      <div class="hero-ctas">
        <button onclick="location.hash='#/catalog'">Browse catalog</button>
        <button class="ghost" onclick="location.hash='#/converter'">Convert</button>
        <button class="ghost" onclick="location.hash='#/doctor'">Diagnose</button>
      </div>
      <div class="hero-meta">
        <div><b>${nagents}</b><span>agents</span></div>
        <div><b>${nskills}</b><span>skills</span></div>
        <div><b>${platsN}</b><span>platforms</span></div>
      </div>
    </div>
  </div>
  ${mq ? `<div class="marquee"><div class="marquee-track">${mq}${mq}</div></div>` : ""}
  <div class="feat-grid">${feats.map(([id, num, t, d], i) => `
    <div class="feat" data-go="#/${id}" style="animation-delay:${0.08 * i}s">
      <span class="go">→</span><div class="fic serif-num">${num}</div><h3>${t}</h3><p>${d}</p>
    </div>`).join("")}
  </div>
  <div class="panel" style="margin-top:16px">
    <h3>Health <span id="vpill"><span class="pill info">CHECKING</span></span></h3>
    <div id="vchecks"><p class="muted">Running quick verify…</p></div>
  </div>`;
};

RENDER["dashboard$mount"] = () => {
  $$(".feat").forEach((f) => {
    f.onclick = () => { location.hash = "#" + f.dataset.go; };
  });
  api("/api/verify?fast=true&skip=adapters,doctor,resolve,why,plan,run,cli")
    .then((v) => {
      const pill = $("#vpill"), box = $("#vchecks");
      if (!pill || !box) return;
      pill.innerHTML = pillFor(v.status);
      box.innerHTML = v.results
        ? `<table><tbody>${v.results.map((r) =>
            `<tr><td>${pillFor(r.status)}</td><td style="font-weight:650">${esc(r.name)}</td>
             <td class="muted">${esc(r.detail || "")}</td></tr>`).join("")}</tbody></table>`
        : `<p class="muted">No check detail.</p>`;
    })
    .catch(() => {
      const pill = $("#vpill");
      if (pill) pill.innerHTML = `<span class="pill warn">UNKNOWN</span>`;
    });
};

/* ---------------- catalog ---------------- */
let catalogCache = [];

let browseState = { type: "all", category: "", q: "", offset: 0, limit: 40 };

RENDER.catalog = async () => {
  let cats = { agent: {}, skill: {} };
  try { cats = await api("/api/categories"); } catch (e) { /* list still works */ }
  const catBtns = (kind) => {
    const entries = Object.entries(cats[kind] || {});
    const total = entries.reduce((a, [, n]) => a + n, 0);
    return `<button class="chip${browseState.category === "" ? " on" : ""}" data-cat="">all<span class="n">${total}</span></button>` +
      entries.map(([c, n]) =>
        `<button class="chip${browseState.category === c ? " on" : ""}" data-cat="${esc(c)}">${esc(c)}<span class="n">${n}</span></button>`).join("");
  };
  return `
  <div class="ph-kicker">01 — Index</div><h1 class="ph-title">The <em>catalog.</em></h1>
  <p class="lede">Every agent &amp; skill, browsable by category. Click a row for details.</p>
  <div class="panel">
    <div class="row">
      <div class="ac-wrap"><input type="text" id="q" placeholder="Filter by name…" value="${esc(browseState.q)}" autocomplete="off"><div class="ac-list" id="ac" style="display:none"></div></div>
      <button id="go">Filter</button>
    </div>
    <div class="checks" style="margin-top:10px">
      <label><input type="radio" name="kind" value="all"${browseState.type === "all" ? " checked" : ""}> all</label>
      <label><input type="radio" name="kind" value="agent"${browseState.type === "agent" ? " checked" : ""}> agents</label>
      <label><input type="radio" name="kind" value="skill"${browseState.type === "skill" ? " checked" : ""}> skills</label>
    </div>
  </div>
  <div class="browse-wrap">
    <div class="panel"><h3>Categories</h3><div class="catlist" id="catlist">${catBtns(browseState.type === "skill" ? "skill" : "agent")}</div></div>
    <div class="panel"><div id="browselist"><p class="muted">Loading…</p></div>
      <div class="pager"><button class="ghost" id="pg-prev">← Prev</button>
      <span class="muted" id="pg-info"></span>
      <button class="ghost" id="pg-next">Next →</button></div></div>
  </div>
  <div class="panel" style="margin-top:16px"><h3>Official Kdesk implementations</h3>
    <p class="muted" style="font-size:13px;margin-bottom:10px">Runnable reference agents shipped with Kdesk (<span class="mono">.sh</span> / <span class="mono">.py</span>).</p>
    <div id="official-list"><p class="muted">Loading…</p></div></div>`;
};

async function loadBrowse() {
  const box = $("#browselist");
  if (!box) return;
  box.innerHTML = `<p class="muted">Loading…</p>`;
  const s = browseState;
  const qs = `type=${s.type}&category=${encodeURIComponent(s.category)}&q=${encodeURIComponent(s.q)}&limit=${s.limit}&offset=${s.offset}`;
  try {
    const d = await api("/api/browse?" + qs);
    catalogCache = d.items || [];
    const pages = Math.max(1, Math.ceil(d.total / s.limit));
    const cur = Math.floor(s.offset / s.limit) + 1;
    $("#pg-info").textContent = `${d.total} items · page ${cur}/${pages}`;
    $("#pg-prev").disabled = s.offset <= 0;
    $("#pg-next").disabled = s.offset + s.limit >= d.total;
    box.innerHTML = catalogCache.length ? `<table><thead><tr><th>Type</th><th>Name</th><th>Category</th><th>Description</th></tr></thead>
      <tbody>${catalogCache.map((h, i) =>
        `<tr class="result-row" data-i="${i}"><td><span class="pill info">${h.type}</span></td>
         <td class="mono">${esc(h.name)}</td><td class="muted">${esc(h.category || "")}</td>
         <td class="muted">${esc((h.description || "").slice(0, 90))}</td></tr>`).join("")}</tbody></table>`
      : emptyState("Nothing here — try another filter.");
    $$(".result-row", box).forEach((tr) => {
      tr.onclick = () => showDefinition(catalogCache[+tr.dataset.i]);
    });
  } catch (e) { box.innerHTML = `<p class="muted">${esc(e.message)}</p>`; }
}

RENDER["catalog$mount"] = () => {
  const q = $("#q"), ac = $("#ac");
  let acTimer = null, acItems = [];
  const hideAc = () => { ac.style.display = "none"; };
  const suggest = () => {
    clearTimeout(acTimer);
    const term = q.value.trim();
    if (term.length < 2) { hideAc(); return; }
    acTimer = setTimeout(async () => {
      try {
        const kind = (document.querySelector('input[name="kind"]:checked') || {}).value || "all";
        acItems = await api("/api/search?q=" + encodeURIComponent(term) + "&limit=8&type=" + kind);
        if (!acItems.length || document.activeElement !== q) { hideAc(); return; }
        ac.innerHTML = acItems.map((h, i) =>
          `<div class="ac-item" data-i="${i}"><span class="pill info">${h.type}</span><span class="mono">${esc(h.name)}</span></div>`).join("");
        ac.style.display = "";
        $$(".ac-item", ac).forEach((el) => {
          el.onclick = () => {
            const h = acItems[+el.dataset.i];
            browseState.q = h.name;
            browseState.offset = 0;
            q.value = h.name;
            hideAc();
            loadBrowse();
          };
        });
      } catch (e) { hideAc(); }
    }, 250);
  };
  q.addEventListener("input", suggest);
  q.addEventListener("blur", () => setTimeout(hideAc, 150));
  q.addEventListener("focus", () => { if (q.value.trim().length >= 2) suggest(); });
  const apply = () => {
    browseState.q = q.value.trim();
    browseState.offset = 0;
    loadBrowse();
  };
  $("#go").onclick = apply;
  q.onkeydown = (e) => { if (e.key === "Enter") apply(); };
  $$('input[name="kind"]').forEach((r) => {
    r.onchange = () => {
      browseState.type = document.querySelector('input[name="kind"]:checked').value;
      browseState.category = "";
      browseState.offset = 0;
      route();
    };
  });
  $$("#catlist .chip").forEach((c) => {
    c.onclick = () => {
      browseState.category = c.dataset.cat;
      browseState.offset = 0;
      $$("#catlist .chip").forEach((x) => x.classList.toggle("on", x === c));
      loadBrowse();
    };
  });
  $("#pg-prev").onclick = () => {
    browseState.offset = Math.max(0, browseState.offset - browseState.limit);
    loadBrowse();
  };
  $("#pg-next").onclick = () => {
    browseState.offset += browseState.limit;
    loadBrowse();
  };
  loadBrowse();
  loadOfficial();
  setTimeout(() => q.focus(), 100);
};

async function loadOfficial() {
  const box = $("#official-list");
  if (!box) return;
  try {
    const d = await api("/api/official");
    const items = d.items || [];
    if (!items.length) { box.innerHTML = `<p class="muted">No runnable implementations found.</p>`; return; }
    box.innerHTML = `<table><thead><tr><th>Name</th><th>Language</th><th>Description</th><th></th></tr></thead><tbody>` +
      items.map((o, i) =>
        `<tr><td class="mono">${esc(o.name)}</td><td><span class="pill info">${esc(o.language)}</span></td>
         <td class="muted">${esc(o.description || o.path)}</td>
         <td><button class="ghost" data-off="${i}">View</button></td></tr>`).join("") +
      `</tbody></table>`;
    box._items = items;
    $$("[data-off]", box).forEach((b) => {
      b.onclick = async () => {
        const o = box._items[+b.dataset.off];
        try {
          const f = await api("/api/official/file?path=" + encodeURIComponent(o.path.replace(/^agents\//, "")));
          openModal(`<h2 class="mono">${esc(o.path)}</h2>
            <pre class="out" style="margin-top:12px;max-height:60vh">${esc(f.content)}</pre>
            <div class="row" style="margin-top:14px"><button class="ghost" onclick="closeModal()">Close</button></div>`);
        } catch (e) { toast(e.message); }
      };
    });
  } catch (e) { box.innerHTML = `<p class="muted">${esc(e.message)}</p>`; }
}

async function showDefinition(h) {
  openModal(`<p class="muted">Loading…</p>`);
  try {
    const [d, links] = await Promise.all([
      api(`/api/definition/${h.type}/${encodeURIComponent(h.name)}`),
      h.type === "agent"
        ? api(`/api/graph?agent=${encodeURIComponent(h.name)}`).catch(() => [])
        : Promise.resolve([]),
    ]);
    const caps = (d.capabilities || []).map((c) =>
      `<tr><td class="mono">${esc(c.name || "")}</td><td>${esc(c.description || "")}</td></tr>`).join("");
    const linkChips = (links || []).slice(0, 24).map((l) =>
      `<span class="pill info" style="margin:0 6px 6px 0">${esc(l.skill || l)}</span>`).join("");
    const platKeys = d.platforms && typeof d.platforms === "object"
      ? Object.keys(d.platforms).slice(0, 20) : [];
    const platChips = platKeys.map((p) =>
      `<span class="pill ok" style="margin:0 6px 6px 0">${esc(p)}</span>`).join("");
    const instr = String(d.instructions || "");
    openModal(`
      <h2 class="mono">${esc(d.name || h.name)}</h2>
      <p class="muted">${esc(d.display_name || "")} · v${esc(d.version || "?")} · ${esc(d.category || "")}</p>
      <p style="margin:12px 0">${esc(d.description || "")}</p>
      ${platChips ? `<div style="margin-bottom:12px"><div class="muted" style="font-size:12px;margin-bottom:6px">PLATFORMS</div>${platChips}</div>` : ""}
      ${linkChips ? `<div style="margin-bottom:12px"><div class="muted" style="font-size:12px;margin-bottom:6px">LINKED SKILLS</div>${linkChips}</div>` : ""}
      ${instr ? `<div class="muted" style="font-size:12px;margin-bottom:6px">INSTRUCTIONS</div><pre class="out" style="max-height:180px">${esc(instr.slice(0, 1500))}</pre>` : ""}
      ${caps ? `<table style="margin-top:12px"><thead><tr><th>Capability</th><th>Description</th></tr></thead><tbody>${caps}</tbody></table>` : ""}
      <div class="row" style="margin-top:16px">
        <button class="ghost" onclick="closeModal()">Close</button>
      </div>`);
  } catch (e) { openModal(`<p class="muted">${esc(e.message)}</p>`); }
}
window.closeModal = closeModal;

/* ---------------- converter ---------------- */
RENDER.converter = async () => {
  const plats = await api("/api/platforms").catch(() => []);
  const opts = plats.map((p) => `<label title="${esc(p.name || p.id)}"><input type="checkbox" value="${p.id}"${["cursor", "claude_code"].includes(p.id) ? " checked" : ""}> ${esc(p.id)}</label>`).join("");
  return `
  <div class="ph-kicker">02 — Transform</div><h1 class="ph-title">Ship <em>everywhere.</em></h1>
  <p class="lede">Pick definitions, upload your own, or convert the whole catalog — with live proof.</p>
  <div class="panel"><h3>1 · Pick definitions <span class="muted" style="font-weight:400">agents &amp; skills</span></h3>
    <div class="row">
      <div class="ac-wrap"><input type="text" id="pk" placeholder="Type a name — kubernetes, terraform…" autocomplete="off"><div class="ac-list" id="pkac" style="display:none"></div></div>
      <button id="pkadd" class="ghost">Add</button>
    </div>
    <div class="checks" style="margin-top:10px">
      <label><input type="radio" name="pkkind" value="all" checked> both</label>
      <label><input type="radio" name="pkkind" value="agent"> agents only</label>
      <label><input type="radio" name="pkkind" value="skill"> skills only</label>
    </div>
    <div class="chips" id="picked" style="margin-top:10px"><span class="muted" style="font-size:13px">nothing picked yet</span></div>
    <div class="row" style="margin-top:12px"><button id="pkgo">Convert picked</button><span id="pkout" class="muted"></span></div>
  </div>
  <div class="panel"><h3>2 · Platforms</h3>
    <div class="plat-grid" id="plats">${opts || '<span class="muted">failed to load platforms</span>'}</div>
    <div class="row" style="margin-top:14px">
      <button id="vbtn" class="ghost">Validate catalog</button><span id="vout" class="muted"></span>
      <button id="cbtn" class="ghost">Convert whole catalog</button><span id="cout" class="muted"></span>
    </div>
  </div>
  <div class="panel"><h3>3 · Or your own files</h3>
    <p class="muted" style="font-size:13px;margin-bottom:10px">Drop agent/skill <span class="mono">.yaml</span> files (max 20, 200KB each) — converted instantly, nothing saved.</p>
    <div class="row"><input type="file" id="upfiles" accept=".yaml,.yml" multiple style="flex:1">
    <button id="ubtn" class="ghost">Convert uploads</button></div>
  </div>
  <div class="panel" id="cres" style="display:none"><h3>Live proof</h3><div id="cbody"></div></div>`;
};

function downloadArtifact(path, content) {
  const blob = new Blob([content], { type: "text/plain" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = path.split("/").pop() || "artifact.txt";
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
  toast("Downloaded " + a.download);
}
window.downloadArtifact = downloadArtifact;

function downloadServerFile(platform, path) {
  const a = document.createElement("a");
  a.href = `/api/convert/file?platform=${encodeURIComponent(platform)}&path=${encodeURIComponent(path)}`;
  a.download = path.split("/").pop() || "artifact.txt";
  document.body.appendChild(a);
  a.click();
  a.remove();
  toast("Downloaded " + a.download);
}
window.downloadServerFile = downloadServerFile;

let artifactStore = [];
function artifactKind(a) {
  const s = (a.source || a.path || "").replace(/\\/g, "/");
  return (s.includes("/skill/") || s.endsWith("-skill.yaml") || s.includes("SKILL.md")) ? "skill" : "agent";
}
/* Live proof: source definition side-by-side with what it became. */
async function renderProof(list, names) {
  artifactStore = list;
  const box = $("#cres");
  box.style.display = "";
  const body = $("#cbody");
  const oks = list.filter((a) => !a.error), errs = list.filter((a) => a.error);
  const bySrc = {};
  oks.forEach((a) => { (bySrc[a.source] = bySrc[a.source] || []).push(a); });
  // fetch source YAMLs for the side-by-side view (best effort)
  const sources = {};
  await Promise.all(names.map(async (n) => {
    try {
      const hit = await api("/api/search?q=" + encodeURIComponent(n) + "&limit=3");
      const exact = (hit || []).find((h) => h.name === n) || hit[0];
      if (!exact) return;
      const d = await api(`/api/definition/${exact.type}/${encodeURIComponent(exact.name)}`);
      const keep = {};
      ["name", "display_name", "category", "description", "version", "tags",
       "capabilities", "instructions", "platforms"].forEach((k) => { if (d[k] !== undefined) keep[k] = d[k]; });
      sources[n] = { type: exact.type, yaml: JSON.stringify(keep, null, 2).slice(0, 2500) };
    } catch (e) { /* proof still renders without source */ }
  }));
  body.innerHTML = `
    <p class="muted" style="margin-bottom:10px">${oks.length} file(s) from ${names.length} definition(s)${errs.length ? ` · ${errs.length} error(s)` : ""}</p>
    <div class="row" style="margin-bottom:12px"><button class="ghost" id="dl-all">Download all (.json bundle)</button></div>
    ${names.map((n) => {
      const arts = bySrc[n] || [];
      const src = sources[n];
      return `<div class="proof"><div class="k">${esc(n)}${src ? ` · ${esc(src.type)}` : ""} → ${arts.length} file(s)</div>
        ${src ? `<pre class="out" style="max-height:150px;margin-top:8px">source ⬇\n${esc(src.yaml)}</pre>` : ""}
        ${arts.map((a) => {
          const idx = list.indexOf(a);
          return `<div class="row" style="gap:8px;margin-top:8px">
            <span class="pill info">${esc(a.platform)}</span>
            <span class="pill info">${artifactKind(a)}</span>
            <span class="mono">${esc(a.path)}</span>
            <button class="ghost" data-dl="${idx}">Download</button>
            <button class="ghost" data-view="${idx}">View</button></div>`;
        }).join("") || `<div class="muted" style="font-size:13px">no outputs — see errors below</div>`}
      </div>`;
    }).join("")}
    ${errs.length ? `<pre class="out" style="margin-top:10px">${esc(errs.map((e) => `${e.source}: ${e.error}`).join("\n"))}</pre>` : ""}
    <pre class="out" id="aview" style="margin-top:10px"></pre>`;
  const showInto = (a) => {
    const v = $("#aview");
    v.style.display = "";
    v.textContent = `--- ${a.platform}/${a.path} [${artifactKind(a)}] ---\n\n${a.content.slice(0, 5000)}`;
    v.scrollIntoView({ block: "nearest" });
  };
  const first = oks[0];
  if (first) showInto(first);
  $("#dl-all").onclick = () => {
    const blob = new Blob([JSON.stringify({ exported_by: "kdesk", artifacts: list }, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "kdesk-convert-bundle.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
    toast("Bundle downloaded");
  };
  $$("#cbody [data-dl]").forEach((b) => {
    b.onclick = () => {
      const a = artifactStore[+b.dataset.dl];
      downloadArtifact(a.path, a.content);
    };
  });
  $$("#cbody [data-view]").forEach((b) => {
    b.onclick = () => showInto(artifactStore[+b.dataset.view]);
  });
}
function renderArtifacts(list) {
  artifactStore = list;
  const box = $("#cres");
  box.style.display = "";
  const oks = list.filter((a) => !a.error), errs = list.filter((a) => a.error);
  const byPlat = {};
  oks.forEach((a) => { (byPlat[a.platform] = byPlat[a.platform] || []).push(a); });
  $("#cbody").innerHTML = `
    <p class="muted" style="margin-bottom:10px">${oks.length} file(s) generated${errs.length ? ` · ${errs.length} error(s)` : ""}</p>
    <div class="row" style="margin-bottom:12px"><button class="ghost" id="dl-all">Download all (.json bundle)</button></div>
    ${Object.entries(byPlat).map(([p, arr]) => `
      <div class="proof"><div class="k">${esc(p)} · ${arr.length} files</div>
      ${arr.slice(0, 30).map((a) => {
        const idx = list.indexOf(a);
        return `<div class="row" style="gap:8px;margin-top:6px">
          <span class="pill info">${artifactKind(a)}</span>
          <span class="mono">${esc(a.path)}</span>
          <button class="ghost" data-dl="${idx}">Download</button>
          <button class="ghost" data-view="${idx}">View</button></div>`;
      }).join("")}
      ${arr.length > 30 ? `<div class="muted" style="font-size:12px">…and ${arr.length - 30} more</div>` : ""}</div>`).join("")}
    ${errs.length ? `<pre class="out" style="margin-top:10px">${esc(errs.map((e) => `${e.source}: ${e.error}`).join("\n"))}</pre>` : ""}
    <pre class="out" id="aview" style="margin-top:10px"></pre>`;
  const showFirst = () => {
    const first = oks[0];
    if (!first) { $("#aview").style.display = "none"; return; }
    const v = $("#aview");
    v.style.display = "";
    v.textContent = `--- ${first.platform}/${first.path} [${artifactKind(first)}] ---\n\n${first.content.slice(0, 5000)}`;
  };
  showFirst();
  $("#dl-all").onclick = () => {
    const blob = new Blob([JSON.stringify({ exported_by: "kdesk", artifacts: list }, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "kdesk-convert-bundle.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
    toast("Bundle downloaded");
  };
  $$("#cbody [data-dl]").forEach((b) => {
    b.onclick = () => {
      const a = artifactStore[+b.dataset.dl];
      downloadArtifact(a.path, a.content);
    };
  });
  $$("#cbody [data-view]").forEach((b) => {
    b.onclick = () => {
      const a = artifactStore[+b.dataset.view];
      const v = $("#aview");
      v.style.display = "";
      v.textContent = `--- ${a.path} ---\n\n${a.content.slice(0, 5000)}`;
      v.scrollIntoView({ block: "nearest" });
    };
  });
}

RENDER["converter$mount"] = () => {
  const picked = []; // [{name, type}]
  const pk = $("#pk"), pkac = $("#pkac"), pickedBox = $("#picked");
  const pkKind = () => (document.querySelector('input[name="pkkind"]:checked') || {}).value || "all";
  let pkTimer = null, pkItems = [];
  const paintPicked = () => {
    pickedBox.innerHTML = picked.length
      ? `<span class="muted" style="font-size:12.5px;margin-right:4px">${picked.length} picked:</span>` +
        picked.map((h, i) => `<button class="chip on" data-unpick="${i}"><span class="pill info">${h.type}</span> ${esc(h.name)} ✕</button>`).join("")
      : `<span class="muted" style="font-size:13px">nothing picked yet — search above, or convert the whole catalog below</span>`;
    $$("[data-unpick]", pickedBox).forEach((c) => {
      c.onclick = () => { picked.splice(+c.dataset.unpick, 1); paintPicked(); };
    });
  };
  const suggestPk = () => {
    clearTimeout(pkTimer);
    const term = pk.value.trim();
    if (term.length < 2) { pkac.style.display = "none"; return; }
    pkTimer = setTimeout(async () => {
      try {
        pkItems = await api("/api/search?q=" + encodeURIComponent(term) + "&limit=8&type=" + pkKind());
        if (!pkItems.length || document.activeElement !== pk) { pkac.style.display = "none"; return; }
        pkac.innerHTML = pkItems.map((h, i) =>
          `<div class="ac-item" data-i="${i}"><span class="pill info">${h.type}</span><span class="mono">${esc(h.name)}</span><span class="muted" style="font-size:12px">${esc(h.category || "")}</span></div>`).join("");
        pkac.style.display = "";
        $$(".ac-item", pkac).forEach((el) => {
          el.onclick = () => {
            const h = pkItems[+el.dataset.i];
            if (!picked.some((p) => p.name === h.name) && picked.length < 25)
              picked.push({ name: h.name, type: h.type });
            pk.value = "";
            pkac.style.display = "none";
            paintPicked();
          };
        });
      } catch (e) { pkac.style.display = "none"; }
    }, 250);
  };
  pk.addEventListener("input", suggestPk);
  pk.addEventListener("blur", () => setTimeout(() => { pkac.style.display = "none"; }, 150));
  const addTyped = async () => {
    const v = pk.value.trim();
    if (!v || picked.some((p) => p.name === v) || picked.length >= 25) { pk.value = ""; paintPicked(); return; }
    let type = pkKind();
    if (type === "all") {
      try {
        const hit = await api("/api/search?q=" + encodeURIComponent(v) + "&limit=3");
        const exact = (hit || []).find((h) => h.name === v) || hit[0];
        if (exact) type = exact.type;
      } catch (e) { /* fall through with generic label */ }
    }
    picked.push({ name: v, type: type === "all" ? "?" : type });
    pk.value = "";
    paintPicked();
  };
  $("#pkadd").onclick = addTyped;
  pk.onkeydown = (e) => { if (e.key === "Enter") addTyped(); };
  paintPicked();
  $("#pkgo").onclick = async (e) => {
    if (!picked.length) { toast("Pick at least one definition above"); return; }
    const sel = $$("#plats input:checked").map((c) => c.value);
    if (!sel.length) { toast("Pick at least one platform"); return; }
    const b = e.target; setBusy(b, true, `Converting ${picked.length}…`);
    try {
      const d = await api("/api/convert-selected", { method: "POST",
        body: JSON.stringify({ names: picked.map((p) => p.name), platforms: sel }) });
      renderProof(d.artifacts || [], picked.map((p) => p.name));
      $("#pkout").textContent = "Done — proof below";
      toast("Conversion complete");
    } catch (err) { toast(err.message); } finally { setBusy(b, false); }
  };
  $("#vbtn").onclick = async (e) => {
    const b = e.target; setBusy(b, true, "Validating…");
    try {
      const d = await api("/api/validate", { method: "POST", body: "{}" });
      $("#vout").textContent = d.valid ? "All definitions valid" : "Validation failed";
      toast(d.valid ? "Catalog valid" : "Validation failed");
    } catch (err) { toast(err.message); } finally { setBusy(b, false); }
  };
  $("#cbtn").onclick = async (e) => {
    const sel = $$("#plats input:checked").map((c) => c.value);
    if (!sel.length) { toast("Pick at least one platform"); return; }
    const b = e.target; setBusy(b, true, `Converting ${sel.length}…`);
    try {
      const d = await api("/api/convert", { method: "POST", body: JSON.stringify({ platforms: sel }) });
      $("#cres").style.display = "";
      const total = Object.values(d.files || {}).reduce((a, n) => a + n, 0);
      const samples = d.sample_paths || {};
      $("#cbody").innerHTML = `
        <p class="muted" style="margin-bottom:10px">${total} files written to <span class="mono">platform-agents/</span></p>
        ${Object.entries(d.files || {}).map(([p, n]) => `
          <div class="proof"><div class="k">${esc(p)} · ${n} files</div>
          ${(samples[p] || []).slice(0, 12).map((fp) =>
            `<div class="row" style="gap:8px;margin-top:6px"><span class="mono">${esc(fp)}</span>
             <button class="ghost" onclick="downloadServerFile('${esc(p)}','${esc(fp)}')">Download</button></div>`).join("")}
          ${n > 12 ? `<div class="muted" style="font-size:12px">…and ${n - 12} more on disk</div>` : ""}</div>`).join("")}`;
      $("#cout").textContent = "Done";
      toast("Conversion complete");
    } catch (err) { toast(err.message); } finally { setBusy(b, false); }
  };
  $("#ubtn").onclick = async (e) => {
    const files = $("#upfiles").files;
    if (!files.length) { toast("Choose .yaml files first"); return; }
    const sel = $$("#plats input:checked").map((c) => c.value);
    if (!sel.length) { toast("Pick at least one platform above"); return; }
    const b = e.target; setBusy(b, true, "Converting…");
    try {
      const fd = new FormData();
      for (const f of files) fd.append("files", f);
      fd.append("platforms", sel.join(","));
      const res = await fetch("/api/convert-upload", { method: "POST", body: fd });
      const d = await res.json();
      if (!res.ok) throw new Error(d.error || "upload failed");
      renderArtifacts(d.artifacts || []);
      toast(`${d.artifacts ? d.artifacts.length : 0} artifacts ready`);
    } catch (err) { toast(err.message); } finally { setBusy(b, false); }
  };
};

/* ---------------- doctor ---------------- */
RENDER.doctor = async () => {
  const plats = await api("/api/platforms").catch(() => []);
  const opts = plats.map((p) => `<option value="${p.id}"${p.id === "claude_code" ? " selected" : ""}>${esc(p.id)}</option>`).join("");
  return `
  <div class="ph-kicker">03 — Diagnose</div><h1 class="ph-title">Proof, <em>not promises.</em></h1>
  <p class="lede">Three steps: pick a platform, pick an action, run.</p>
  <div class="panel"><div class="step-h"><span class="n">i.</span><h3>Target platform</h3></div>
    <div class="chips" id="dplats">${plats.length ? plats.map((p) =>
      `<button class="chip${p.id === "claude_code" ? " on" : ""}" data-plat="${esc(p.id)}" title="${esc(p.name || p.id)}">${esc(p.id)}</button>`).join("")
      : '<span class="muted" style="font-size:13px">Could not load platforms — restart the server and refresh.</span>'}</div>
  </div>
  <div class="panel"><div class="step-h"><span class="n">ii.</span><h3>Action</h3></div>
    <div class="act-grid" id="dacts">
      <button class="act" data-act="check"><span class="tick">✓</span><b>Check</b><span>Is it installed correctly here?</span></button>
      <button class="act" data-act="scan"><span class="tick">✓</span><b>Scan</b><span>What AI configs exist in the project?</span></button>
      <button class="act on" data-act="diagnose"><span class="tick">✓</span><b>Diagnose</b><span>Full health analysis with evidence</span></button>
      <button class="act" data-act="fix"><span class="tick">✓</span><b>Fix</b><span>Apply repairs, previewed first</span></button>
    </div>
  </div>
  <div class="panel"><div class="step-h"><span class="n">iii.</span><h3>Project &amp; run</h3></div>
    <div class="row">
      <input type="text" id="droot" placeholder="Project path (blank = this repo)">
      <label class="muted" style="font-size:13px"><input type="checkbox" id="ddry" checked> preview only (dry-run)</label>
      <button id="dbtn">Run diagnosis</button>
    </div>
  </div>
  <div class="panel"><h3>Or diagnose your own files</h3>
    <p class="muted" style="font-size:13px;margin-bottom:10px">Upload project files (configs, rules, prompts — max 20, 200KB each). Scanned in a temp dir, nothing saved.</p>
    <div class="row"><input type="file" id="dfiles" multiple style="flex:1">
    <select id="dmode2"><option value="scan">scan</option><option value="diagnose">diagnose</option></select>
    <button id="dbtn2" class="ghost">Upload &amp; diagnose</button></div>
  </div>
  <div class="panel" id="dres"><h3>Report</h3><div id="dbody"></div></div>`;
};

function renderDoctorReport(rep, mode, dry) {
  const score = rep.score != null ? rep.score : 100;
  const C = 2 * Math.PI * 34;
  const issues = (rep.issues || []).slice(0, 60);
  const cats = {};
  (rep.issues || []).forEach((i) => { cats[i.category || "other"] = (cats[i.category || "other"] || 0) + 1; });
  const catLine = Object.entries(cats).slice(0, 8).map(([k, v]) =>
    `<span class="pill info" style="margin:0 6px 6px 0">${esc(k)} · ${v}</span>`).join("");
  const scan = rep.scan || rep.scan_metadata || null;
  const proof = scan ? `
    <div class="proof"><div class="k">Detected in project</div><div class="v">${esc(scan.platform || rep.platform || "unknown")} ·
    agents ${scan.agents != null ? (Array.isArray(scan.agents) ? scan.agents.length : scan.agents) : "?"} ·
    skills ${scan.skills != null ? (Array.isArray(scan.skills) ? scan.skills.length : scan.skills) : "?"} ·
    configs ${scan.configuration != null ? (Array.isArray(scan.configuration) ? scan.configuration.length : scan.configuration) : "?"}</div></div>
    <div class="proof"><div class="k">Project root</div><div class="v">${esc(scan.project_root || "")}</div></div>` : "";
  return `
    <div class="ring">
      <svg width="88" height="88"><circle class="bg" cx="44" cy="44" r="34" fill="none" stroke-width="9"/>
      <circle class="fg" cx="44" cy="44" r="34" fill="none" stroke-width="9"
        stroke-dasharray="${C}" stroke-dashoffset="${C}"/></svg>
      <div><div class="pct">${score}%</div><div class="muted">health · ${esc(rep.platform || "")}${mode === "fix" && !dry ? " · applied" : ""}</div></div>
    </div>
    ${proof}
    ${catLine ? `<div style="margin-top:12px">${catLine}</div>` : ""}
    ${issues.length ? `<table style="margin-top:14px"><thead><tr><th>Severity</th><th>File</th><th>Message</th><th>Fix</th></tr></thead>
    <tbody>${issues.map((i) => `<tr><td>${pillFor(i.severity)}</td>
      <td class="mono">${esc(i.file || "")}</td><td>${esc(i.message || "")}</td>
      <td class="muted">${esc(i.suggested_fix || (i.fixable ? "auto-fixable" : "manual"))}</td></tr>`).join("")}</tbody></table>`
    : `<p class="muted" style="margin-top:12px">No issues — this project looks clean for the target platform.</p>`}
    ${rep.fix_report ? `<pre class="out" style="margin-top:12px">${esc(JSON.stringify(rep.fix_report, null, 2).slice(0, 3000))}</pre>` : ""}`;
}

function animateRing() {
  requestAnimationFrame(() => requestAnimationFrame(() => {
    const fg = $("#dbody .fg"), pct = $("#dbody .pct");
    const score = pct ? parseInt(pct.textContent) || 0 : 0;
    if (fg) fg.style.strokeDashoffset = String(2 * Math.PI * 34 * (1 - score / 100));
  }));
}

RENDER["doctor$mount"] = () => {
  $("#dbody").innerHTML = emptyState("No diagnosis yet — pick a platform and action above, then Run.");
  const tick = (b, t0, label) => {
    const h = setInterval(() => {
      if (!b.disabled) { clearInterval(h); return; }
      const s = Math.round((Date.now() - t0) / 1000);
      b.innerHTML = `<span class="spin"></span>${label}… ${s}s`;
    }, 1000);
    return h;
  };
  const selPlat = () => {
    const on = document.querySelector('#dplats .chip.on');
    return on ? on.dataset.plat : "claude_code";
  };
  const selAct = () => {
    const on = document.querySelector('#dacts .act.on');
    return on ? on.dataset.act : "diagnose";
  };
  $$("#dplats .chip").forEach((c) => {
    c.onclick = () => {
      $$("#dplats .chip").forEach((x) => x.classList.toggle("on", x === c));
    };
  });
  $$("#dacts .act").forEach((a) => {
    a.onclick = () => {
      $$("#dacts .act").forEach((x) => x.classList.toggle("on", x === a));
    };
  });
  $("#dbtn").onclick = async (e) => {
    const b = e.target; setBusy(b, true, "Diagnosing…");
    const t0 = Date.now(); tick(b, t0, "Diagnosing");
    const mode = selAct();
    const dry = $("#ddry").checked;
    if (mode === "fix" && !dry && !confirm("Apply fixes for real (not a preview)?")) { setBusy(b, false); return; }
    try {
      const d = await api("/api/doctor", { method: "POST", body: JSON.stringify({
        platform: selPlat(), mode,
        project_root: $("#droot").value.trim() || null, dry_run: dry,
      }) });
      const box = $("#dres"); box.style.display = "";
      const rep = d.report || d;
      $("#dbody").innerHTML = renderDoctorReport(rep, mode, dry);
      animateRing();
    } catch (err) { toast(err.message); } finally { setBusy(b, false); }
  };
  $("#dbtn2").onclick = async (e) => {
    const files = $("#dfiles").files;
    if (!files.length) { toast("Choose files first"); return; }
    const b = e.target; setBusy(b, true, "Uploading…");
    const t0 = Date.now(); tick(b, t0, "Diagnosing");
    try {
      const fd = new FormData();
      for (const f of files) fd.append("files", f);
      fd.append("platform", selPlat());
      fd.append("mode", $("#dmode2").value);
      const res = await fetch("/api/doctor-upload", { method: "POST", body: fd });
      const d = await res.json();
      if (!res.ok) throw new Error(d.error || "upload failed");
      const box = $("#dres"); box.style.display = "";
      const rep = d.report || d;
      rep.scan = rep.scan || null;
      $("#dbody").innerHTML = renderDoctorReport(rep, $("#dmode2").value, true);
      animateRing();
      toast("Upload diagnosed");
    } catch (err) { toast(err.message); } finally { setBusy(b, false); }
  };
};

/* ---------------- marketplace ---------------- */
RENDER.marketplace = async () => {
  const d = await api("/api/skills").catch(() => ({ entries: [], stats: {} }));
  const cards = (d.entries || []).map((s) => `
    <div class="card">
      <div class="mono" style="font-weight:700">${esc(s.name)}</div>
      <div style="margin:6px 0"><span class="pill info">v${esc(s.version)}</span>
      <span class="muted" style="font-size:12.5px;margin-left:8px">${esc(s.category || "")}</span></div>
      <div class="muted" style="font-size:13px;min-height:40px">${esc((s.description || "").slice(0, 110))}</div>
      <div class="row" style="margin-top:10px">
        <button class="ghost" data-resolve="${esc(s.name)}">Resolve</button>
      </div>
    </div>`).join("");
  return `
  <div class="ph-kicker">04 — Exchange</div><h1 class="ph-title">Trade <em>skills.</em></h1>
  <p class="lede">${d.stats.unique_skills || 0} skills · ${d.stats.total_versions || 0} versions</p>
  <div class="skill-grid" style="margin-bottom:16px">${cards || `<div class="card"><p class="muted">Registry is empty.</p></div>`}</div>
  <div class="panel"><h3>Find a skill</h3><div class="row">
    <input type="text" id="sq" placeholder="Search skills…"><button id="sgo">Search</button>
    <input type="text" id="sins" placeholder="name@version to resolve" style="max-width:240px"><button id="sib" class="ghost">Resolve</button>
  </div><div id="sout" style="margin-top:10px"></div></div>
  <div class="panel"><h3>Publish a skill</h3><div class="row">
    <input type="text" id="spub-id" placeholder="skill id from the catalog">
    <label class="muted" style="font-size:13px"><input type="checkbox" id="spub-force"> overwrite existing version</label>
    <button id="spub" class="ghost">Publish</button>
  </div></div>`;
};

RENDER["marketplace$mount"] = () => {
  const showResolved = (d) => {
    $("#sout").innerHTML = `<span class="pill ok">RESOLVED</span>
      <span class="mono" style="margin-left:8px">${esc(d.name)}@${esc(d.version)}</span>
      <span class="muted" style="margin-left:8px">${esc((d.dependencies || []).join(", "))}</span>`;
  };
  const go = async () => {
    const r = await api("/api/skills/search?q=" + encodeURIComponent($("#sq").value.trim())).catch(() => []);
    $("#sout").innerHTML = r.length
      ? r.map((s) => `<div class="row" style="margin-top:6px"><span class="mono">${esc(s.name)}@${esc(s.version)}</span>
        <span class="muted">${esc(s.category || "")}</span></div>`).join("")
      : emptyState("No matching skills in the registry.");
  };
  $("#sgo").onclick = go;
  $("#sq").onkeydown = (e) => { if (e.key === "Enter") go(); };
  $("#sib").onclick = async () => {
    const spec = $("#sins").value.trim();
    if (!spec) return;
    try {
      showResolved(await api("/api/skills/install?spec=" + encodeURIComponent(spec), { method: "POST" }));
    } catch (e) { toast(e.message); }
  };
  $$("[data-resolve]").forEach((b) => {
    b.onclick = async () => {
      try {
        showResolved(await api("/api/skills/install?spec=" + encodeURIComponent(b.dataset.resolve), { method: "POST" }));
      } catch (e) { toast(e.message); }
    };
  });
  $("#spub").onclick = async (e) => {
    const id = $("#spub-id").value.trim();
    if (!id) { toast("Type a skill id first"); return; }
    const b = e.target; setBusy(b, true, "Publishing…");
    try {
      const d = await api("/api/skills/publish", { method: "POST",
        body: JSON.stringify({ skill_id: id, force: $("#spub-force").checked }) });
      toast(`Published ${d.name || id}`);
      route();
    } catch (err) { toast(err.message); } finally { setBusy(b, false); }
  };
};

/* ---------------- install ---------------- */
RENDER.install = async () => {
  const plats = await api("/api/platforms").catch(() => []);
  const opts = plats.map((p) => `<option value="${p.id}"${p.id === "claude_code" ? " selected" : ""}>${esc(p.id)}</option>`).join("");
  return `
  <div class="ph-kicker">05 — Deploy</div><h1 class="ph-title">Put it <em>in place.</em></h1>
  <p class="lede">Install, verify, drift-check, roll back, or remove platform files. Dry-run is on by default.</p>
  <div class="panel"><div class="row">
    <select id="iact">
      <option value="install">install</option><option value="uninstall">uninstall</option>
      <option value="rollback">rollback</option><option value="drift">drift</option>
      <option value="status">status</option>
    </select>
    <select id="iplat">${opts}</select>
    <input type="text" id="iscope" placeholder="scope (optional)" style="max-width:150px">
    <input type="text" id="itool" placeholder="tool (optional)" style="max-width:150px">
    <label class="muted" style="font-size:13px"><input type="checkbox" id="idry" checked> dry-run</label>
    <button id="ibtn">Go</button>
  </div></div>
  <div class="panel" id="ires" style="display:none"><h3>Result</h3><pre class="out" id="ipre"></pre></div>`;
};

RENDER["install$mount"] = () => {
  const show = (d) => {
    $("#ires").style.display = "";
    $("#ipre").textContent = JSON.stringify(d, null, 2).slice(0, 5000);
  };
  $("#ibtn").onclick = async (e) => {
    const act = $("#iact").value, plat = $("#iplat").value;
    const dry = $("#idry").checked;
    if (!dry && (act === "uninstall" || act === "rollback" || (act === "install"))
        && !confirm(`${act} ${plat} for real (dry-run off)?`)) return;
    const b = e.target; setBusy(b, true, "Working…");
    try {
      if (act === "drift") {
        show(await api("/api/drift?platform=" + encodeURIComponent(plat)));
      } else if (act === "status") {
        show(await api("/api/install-status"));
      } else {
        show(await api("/api/" + act, { method: "POST", body: JSON.stringify({
          platform: plat,
          scope: $("#iscope").value.trim() || null,
          tool: $("#itool").value.trim() || null,
          dry_run: dry,
        }) }));
      }
    } catch (err) { toast(err.message); } finally { setBusy(b, false); }
  };
};

/* ---------------- boot ---------------- */
async function ensureCatalog() {
  const t0 = Date.now();
  for (;;) {
    let h;
    try {
      h = await api("/api/health");
    } catch (e) {
      $("#setup-msg").textContent = "Server unreachable. Is `kdesk serve` running?";
      $("#splash").classList.add("done");
      $("#setup").classList.add("show");
      return setupFlow();
    }
    if (h.catalog_ok) return true;
    if (h.status === "warming") {
      const secs = Math.round((Date.now() - t0) / 1000);
      const sub = document.querySelector(".splash-sub");
      if (sub) sub.textContent = `Warming up the catalog… ${secs}s (first run takes ~1 min, later seconds)`;
      await new Promise((r) => setTimeout(r, 2500));
      continue;
    }
    $("#setup-msg").textContent =
      `No catalog found at ${h.root || "this location"}. Paste the path to your Kdesk-Catalog checkout.`;
    $("#splash").classList.add("done");
    $("#setup").classList.add("show");
    return setupFlow();
  }
}

function setupFlow() {
  return new Promise((resolve) => {
    const go = async () => {
      const v = $("#root-input").value.trim();
      if (!v) return;
      try {
        const d = await api("/api/set-root", { method: "POST", body: JSON.stringify({ path: v }) });
        toast(`Loaded ${d.definitions} definitions`);
        $("#setup").classList.remove("show");
        $("#app").classList.add("ready");
        paintGreet();
        resolve(true);
      } catch (err) { toast(err.message); }
    };
    $("#root-go").onclick = go;
    $("#root-input").onkeydown = (e) => { if (e.key === "Enter") go(); };
    setTimeout(() => $("#root-input").focus(), 400);
  });
}

(async function boot() {
  await bootIdentity();
  const ok = await ensureCatalog();
  if (!ok) return;
  if (!location.hash) location.hash = "#/dashboard";
  route();
})();
