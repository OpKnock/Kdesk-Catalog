/* Kdesk dashboard SPA — hash router + API client + pages */
"use strict";

const $ = (sel, root) => (root || document).querySelector(sel);
const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

async function api(path, opts) {
  const res = await fetch(path, Object.assign(
    { headers: { "Content-Type": "application/json" } }, opts || {}));
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((data && data.error) || ("HTTP " + res.status));
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
  return new Promise((resolve) => {
    const done = () => {
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
    ? `Good ${part},<br><b>${esc(n)}</b>`
    : `Kdesk dashboard<br><b>v1.1.0</b>`;
}

/* ---------------- nav + router ---------------- */
const PAGES = [
  ["dashboard", "◈", "Dashboard"],
  ["catalog", "◎", "Catalog"],
  ["quality", "✓", "Quality"],
  ["converter", "⇄", "Converter"],
  ["doctor", "✚", "Doctor"],
  ["marketplace", "▣", "Marketplace"],
  ["engine", "▶", "Engine"],
  ["install", "⬇", "Install"],
  ["tools", "⚙", "Tools"],
];

function paintNav(active) {
  $("#nav").innerHTML = PAGES.map(([id, ico, label]) =>
    `<button class="nav-item${id === active ? " active" : ""}" data-page="${id}">
       <span class="ico">${ico}</span><span class="txt">${label}</span>
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
    main.innerHTML = `<div class="page">${await RENDER[page]()}</div>`;
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
  const [stats, tele] = await Promise.all([
    api("/api/stats?fast=true"),
    api("/api/telemetry").catch(() => null),
  ]);
  const cards = [
    [stats.definitions_total ?? stats.total_files ?? "—", "definitions"],
    [stats.agents ?? "—", "agents"],
    [stats.skills ?? "—", "skills"],
    [stats.platforms ?? "—", "platforms"],
    [stats.workflows ?? "—", "workflows"],
    [stats.platform_output_files ?? "—", "generated files"],
  ];
  const teleLine = tele && tele.total
    ? `<span class="muted"> · ${tele.total} tracked runs</span>` : "";
  return `
    <h1>Dashboard</h1>
    <p class="lede">Catalog health at a glance &nbsp;<span id="vpill"><span class="pill info">CHECKING</span></span>${teleLine}</p>
    <div class="grid">${cards.map(([n, l]) =>
      `<div class="card"><div class="stat-num">${n}</div><div class="stat-label">${l}</div></div>`).join("")}
    </div>
    <div class="panel" style="margin-top:16px;display:none" id="vpanel">
      <h3>Verify checks</h3><div id="vchecks"><p class="muted">Running verify gate…</p></div>
    </div>
    <div class="panel" style="margin-top:16px">
      <h3>Start here</h3>
      <div class="row">
        <button class="ghost" onclick="location.hash='#/catalog'">Browse catalog</button>
        <button class="ghost" onclick="location.hash='#/quality'">Run quality gates</button>
        <button class="ghost" onclick="location.hash='#/doctor'">Diagnose a project</button>
        <button class="ghost" onclick="location.hash='#/converter'">Convert to a platform</button>
        <button class="ghost" id="refresh-btn">Refresh catalog</button>
      </div>
    </div>`;
};

RENDER["dashboard$mount"] = () => {
  const b = $("#refresh-btn");
  if (b) b.onclick = async () => {
    setBusy(b, true, "Refreshing…");
    try {
      await api("/api/refresh", { method: "POST" });
      toast("Catalog reloaded");
      route();
    } catch (e) { toast(e.message); } finally { setBusy(b, false); }
  };
  // verify fills in async — never blocks the cards
  api("/api/verify?fast=true")
    .then((v) => {
      const pill = $("#vpill"), box = $("#vchecks"), panel = $("#vpanel");
      if (!pill) return;
      pill.innerHTML = pillFor(v.status);
      if (panel && box && v.results) {
        panel.style.display = "";
        box.innerHTML = `<table><tbody>${v.results.map((r) =>
          `<tr><td>${pillFor(r.status)}</td><td style="font-weight:650">${esc(r.name)}</td>
           <td class="muted">${esc(r.detail || "")}</td></tr>`).join("")}</tbody></table>`;
      }
    })
    .catch(() => {
      const pill = $("#vpill");
      if (pill) pill.innerHTML = `<span class="pill warn">UNKNOWN</span>`;
    });
};

/* ---------------- catalog ---------------- */
let catalogCache = [];

RENDER.catalog = async () => `
  <h1>Catalog</h1>
  <p class="lede">Search 3,093 agents &amp; skills. Click a row for details.</p>
  <div class="panel">
    <div class="row">
      <input type="text" id="q" placeholder="Try ‘kubernetes’, ‘terraform’, ‘testing’…">
      <button id="go">Search</button>
    </div>
    <div class="checks" id="kindpick" style="margin-top:10px">
      <label><input type="radio" name="kind" value="all" checked> all</label>
      <label><input type="radio" name="kind" value="agent"> agents</label>
      <label><input type="radio" name="kind" value="skill"> skills</label>
    </div>
  </div>
  <div class="panel" id="results"><p class="muted">Type to search.</p></div>`;

RENDER["catalog$mount"] = () => {
  const q = $("#q"), box = $("#results");
  const kind = () => (document.querySelector('input[name="kind"]:checked') || {}).value || "all";
  const run = async () => {
    const term = q.value.trim();
    if (!term) return;
    box.innerHTML = `<p class="muted">Searching…</p>`;
    try {
      catalogCache = await api("/api/search?q=" + encodeURIComponent(term) + "&type=" + kind());
      if (!catalogCache.length) { box.innerHTML = `<p class="muted">No results.</p>`; return; }
      box.innerHTML = `<p class="muted" style="margin-bottom:10px">${catalogCache.length} result(s)</p>
        <table><thead><tr><th>Type</th><th>Name</th><th>Category</th></tr></thead>
        <tbody>${catalogCache.map((h, i) =>
          `<tr class="result-row" data-i="${i}"><td><span class="pill info">${h.type}</span></td>
           <td class="mono">${esc(h.name)}</td><td class="muted">${esc(h.category || "")}</td></tr>`).join("")}
        </tbody></table>`;
      $$(".result-row", box).forEach((tr) => {
        tr.onclick = () => showDefinition(catalogCache[+tr.dataset.i]);
      });
    } catch (e) { box.innerHTML = `<p class="muted">${esc(e.message)}</p>`; }
  };
  $("#go").onclick = run;
  q.onkeydown = (e) => { if (e.key === "Enter") run(); };
  $$('input[name="kind"]').forEach((r) => { r.onchange = () => { if (q.value.trim()) run(); }; });
  setTimeout(() => q.focus(), 100);
};

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

/* ---------------- quality ---------------- */
const GATES = [
  ["verify", "Verify gate", "/api/verify?fast=true", (d) => [d.status, `${d.results ? d.results.filter((r) => r.status === "PASS").length : "?"} checks pass`]],
  ["policy", "Policy (12 rules)", "/api/policy", (d) => [(d.violations && d.violations.length ? "FAIL" : "PASS"), `${d.passed}/${d.total_rules} rules`]],
  ["security", "Secrets scan", "/api/security", (d) => [(d.blocking_count ? "FAIL" : "PASS"), `${d.findings ? d.findings.length : 0} findings, ${d.blocking_count || 0} blocking`]],
  ["quality", "Content quality", "/api/quality", (d) => [(d.low_score_count ? "FAIL" : "PASS"), `${d.files_scanned || "?"} files`]],
  ["duplicates", "Duplicates", "/api/duplicates", (d) => [(d.unresolved_count ? "FAIL" : "PASS"), `${d.unresolved_count || 0} unresolved`]],
  ["license", "Licenses", "/api/license", (d) => [(d.unresolved_count ? "FAIL" : "PASS"), `${d.unresolved_count || 0} unresolved`]],
  ["provenance", "Provenance", "/api/provenance", (d) => [(d.problems && d.problems.length ? "FAIL" : "PASS"), `${d.files_scanned || "?"} files`]],
  ["wiring", "Wiring", "/api/wiring", (d) => [(d.problems && d.problems.length ? "FAIL" : "PASS"), "evidence links"]],
  ["schema", "Schema", "/api/schema", (d) => [(d.exit_code === 0 ? "PASS" : "FAIL"), d.output ? d.output.split("\n").slice(-2).join(" ") : ""]],
];

RENDER.quality = async () => `
  <h1>Quality</h1>
  <p class="lede">Every gate, live. Cards fill in as each gate finishes — click one for raw output.</p>
  <div class="grid" id="gates">${GATES.map(([id, label], i) => `
    <div class="card" data-gate="${id}" style="animation-delay:${0.05 * i}s">
      <div data-slot="pill"><span class="pill info">QUEUED</span></div>
      <div style="font-weight:700;margin:8px 0 2px">${label}</div>
      <div class="muted" data-slot="sub" style="font-size:13px">waiting…</div>
    </div>`).join("")}
  </div>`;

RENDER["quality$mount"] = () => {
  window._gates = window._gates || {};
  GATES.forEach(([id, label, url, fmt]) => {
    api(url).then((d) => {
      const [st, sub] = fmt(d);
      window._gates[id] = d;
      const card = document.querySelector(`[data-gate="${id}"]`);
      if (!card) return;
      card.querySelector('[data-slot="pill"]').innerHTML = pillFor(st);
      card.querySelector('[data-slot="sub"]').textContent = sub;
      card.classList.add("result-row");
      card.onclick = () => openModal(`<h2>${label}</h2>
        <pre class="out" style="margin-top:12px">${esc(JSON.stringify(d, null, 2).slice(0, 6000))}</pre>
        <div class="row" style="margin-top:14px"><button class="ghost" onclick="closeModal()">Close</button></div>`);
    }).catch((e) => {
      const card = document.querySelector(`[data-gate="${id}"]`);
      if (!card) return;
      card.querySelector('[data-slot="pill"]').innerHTML = pillFor("ERROR");
      card.querySelector('[data-slot="sub"]').textContent = e.message;
    });
  });
};

/* ---------------- converter ---------------- */
RENDER.converter = async () => {
  const plats = await api("/api/platforms").catch(() => []);
  const opts = plats.map((p) => `<label><input type="checkbox" value="${p.id}"> ${esc(p.id)}</label>`).join("");
  return `
  <h1>Converter</h1>
  <p class="lede">Generate platform-native files from the universal catalog.</p>
  <div class="panel"><h3>1 · Validate sources</h3>
    <div class="row"><button id="vbtn" class="ghost">Validate 3,093 definitions</button><span id="vout" class="muted"></span></div>
  </div>
  <div class="panel"><h3>2 · Pick platforms &amp; convert</h3>
    <div class="checks" id="plats">${opts || '<span class="muted">failed to load platforms</span>'}</div>
    <div class="row" style="margin-top:14px"><button id="cbtn">Convert</button><span id="cout" class="muted"></span></div>
  </div>
  <div class="panel" id="cres" style="display:none"><h3>Result</h3><pre class="out" id="cpre"></pre></div>`;
};

RENDER["converter$mount"] = () => {
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
      $("#cpre").textContent = JSON.stringify(d, null, 2);
      $("#cout").textContent = "Done";
      toast("Conversion complete");
    } catch (err) { toast(err.message); } finally { setBusy(b, false); }
  };
};

/* ---------------- doctor ---------------- */
RENDER.doctor = async () => {
  const plats = await api("/api/platforms").catch(() => []);
  const opts = plats.map((p) => `<option value="${p.id}">${esc(p.id)}</option>`).join("");
  return `
  <h1>Doctor</h1>
  <p class="lede">Scan any project, diagnose issues, preview fixes.</p>
  <div class="panel">
    <div class="row">
      <select id="dplat">${opts}</select>
      <select id="dmode">
        <option value="check">check</option><option value="scan">scan</option>
        <option value="diagnose">diagnose</option><option value="fix">fix</option>
      </select>
      <input type="text" id="droot" placeholder="Project path (blank = this repo)">
      <label class="muted" style="font-size:13px"><input type="checkbox" id="ddry" checked> preview only (dry-run)</label>
      <button id="dbtn">Run</button>
    </div>
  </div>
  <div class="panel" id="dres" style="display:none"><h3>Report</h3><div id="dbody"></div></div>`;
};

RENDER["doctor$mount"] = () => {
  $("#dbtn").onclick = async (e) => {
    const b = e.target; setBusy(b, true, "Diagnosing…");
    const mode = $("#dmode").value;
    const dry = $("#ddry").checked;
    if (mode === "fix" && !dry && !confirm("Apply fixes for real (not a preview)?")) { setBusy(b, false); return; }
    try {
      const d = await api("/api/doctor", { method: "POST", body: JSON.stringify({
        platform: $("#dplat").value, mode,
        project_root: $("#droot").value.trim() || null, dry_run: dry,
      }) });
      const box = $("#dres"); box.style.display = "";
      const rep = d.report || d;
      const score = rep.score != null ? rep.score : 100;
      const C = 2 * Math.PI * 34;
      const issues = (rep.issues || []).slice(0, 60);
      const cats = {};
      (rep.issues || []).forEach((i) => { cats[i.category || "other"] = (cats[i.category || "other"] || 0) + 1; });
      const catLine = Object.entries(cats).slice(0, 8).map(([k, v]) =>
        `<span class="pill info" style="margin:0 6px 6px 0">${esc(k)} · ${v}</span>`).join("");
      $("#dbody").innerHTML = `
        <div class="ring">
          <svg width="88" height="88"><circle class="bg" cx="44" cy="44" r="34" fill="none" stroke-width="9"/>
          <circle class="fg" cx="44" cy="44" r="34" fill="none" stroke-width="9"
            stroke-dasharray="${C}" stroke-dashoffset="${C}"/></svg>
          <div><div class="pct">${score}%</div><div class="muted">health · ${esc(rep.platform || "")}${mode === "fix" && !dry ? " · applied" : ""}</div></div>
        </div>
        ${catLine ? `<div style="margin-top:12px">${catLine}</div>` : ""}
        ${issues.length ? `<table style="margin-top:14px"><thead><tr><th>Severity</th><th>File</th><th>Message</th></tr></thead>
        <tbody>${issues.map((i) => `<tr><td>${pillFor(i.severity)}</td>
          <td class="mono">${esc(i.file || "")}</td><td>${esc(i.message || "")}</td></tr>`).join("")}</tbody></table>` : ""}
        ${rep.fix_report ? `<pre class="out" style="margin-top:12px">${esc(JSON.stringify(rep.fix_report, null, 2).slice(0, 3000))}</pre>` : ""}`;
      requestAnimationFrame(() => requestAnimationFrame(() => {
        const fg = $("#dbody .fg");
        if (fg) fg.style.strokeDashoffset = String(C * (1 - score / 100));
      }));
    } catch (err) { toast(err.message); } finally { setBusy(b, false); }
  };
};

/* ---------------- marketplace ---------------- */
RENDER.marketplace = async () => {
  const d = await api("/api/skills").catch(() => ({ entries: [], stats: {} }));
  const rows = (d.entries || []).map((s) =>
    `<tr><td class="mono">${esc(s.name)}@${esc(s.version)}</td><td>${esc(s.category || "")}</td>
     <td class="muted">${esc((s.description || "").slice(0, 80))}</td></tr>`).join("");
  return `
  <h1>Marketplace</h1>
  <p class="lede">${d.stats.unique_skills || 0} skills · ${d.stats.total_versions || 0} versions</p>
  <div class="panel"><div class="row">
    <input type="text" id="sq" placeholder="Search skills…"><button id="sgo">Search</button>
    <input type="text" id="sins" placeholder="name@version to resolve" style="max-width:240px"><button id="sib" class="ghost">Resolve</button>
  </div></div>
  <div class="panel"><h3>Publish a skill</h3><div class="row">
    <input type="text" id="spub-id" placeholder="skill id from the catalog">
    <label class="muted" style="font-size:13px"><input type="checkbox" id="spub-force"> overwrite existing version</label>
    <button id="spub" class="ghost">Publish</button>
  </div></div>
  <div class="panel"><table><thead><tr><th>Skill</th><th>Category</th><th>Description</th></tr></thead>
  <tbody id="srows">${rows}</tbody></table></div>`;
};

RENDER["marketplace$mount"] = () => {
  const go = async () => {
    const r = await api("/api/skills/search?q=" + encodeURIComponent($("#sq").value.trim())).catch(() => []);
    $("#srows").innerHTML = r.map((s) =>
      `<tr><td class="mono">${esc(s.name)}@${esc(s.version)}</td><td>${esc(s.category || "")}</td>
       <td class="muted">${esc((s.description || "").slice(0, 80))}</td></tr>`).join("") || `<tr><td colspan="3" class="muted">No results.</td></tr>`;
  };
  $("#sgo").onclick = go;
  $("#sq").onkeydown = (e) => { if (e.key === "Enter") go(); };
  $("#sib").onclick = async () => {
    const spec = $("#sins").value.trim();
    if (!spec) return;
    try {
      const d = await api("/api/skills/install?spec=" + encodeURIComponent(spec), { method: "POST" });
      toast(`Resolved ${d.name}@${d.version}`);
    } catch (e) { toast(e.message); }
  };
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

/* ---------------- engine ---------------- */
RENDER.engine = async () => {
  const h = await api("/api/history?limit=8").catch(() => []);
  const rows = (h || []).map((x, i) =>
    `<tr class="result-row" data-id="${esc(x.execution_id || "")}">
     <td class="mono">${esc((x.execution_id || "").slice(0, 12))}</td>
     <td>${esc(x.request || "")}</td><td>${pillFor(x.status)}</td></tr>`).join("");
  return `
  <h1>Engine</h1>
  <p class="lede">Resolve intent, plan, and run executions. Click a row to inspect.</p>
  <div class="panel"><h3>Ask</h3>
    <div class="row"><input type="text" id="eq" placeholder="e.g. lint my terraform code">
      <button id="eb1">Resolve</button><button id="eb2" class="ghost">Plan</button>
      <button id="eb3" class="ghost">Dry-run</button></div>
    <div class="row" style="margin-top:10px">
      <label class="muted" style="font-size:13px"><input type="checkbox" id="eexec"> execute for real (not a dry-run)</label>
      <label class="muted" style="font-size:13px"><input type="checkbox" id="eauto"> auto-approve steps</label>
    </div>
  </div>
  <div class="panel" id="eres" style="display:none"><h3>Result</h3><div id="ebody"></div>
    <div class="row" id="eactions" style="margin-top:12px"></div></div>
  <div class="panel"><h3>Recent executions</h3>
    <table><thead><tr><th>ID</th><th>Request</th><th>Status</th></tr></thead>
    <tbody id="ehist">${rows || `<tr><td colspan="3" class="muted">None yet.</td></tr>`}</tbody></table></div>`;
};

async function inspectExecution(id) {
  openModal(`<p class="muted">Loading execution…</p>`);
  try {
    const d = await api(`/api/inspect/${encodeURIComponent(id)}`);
    const ex = d.execution || {};
    const step = ex.approval_step;
    const waiting = ex.status === "WAITING_APPROVAL" || ex.status === "PENDING";
    openModal(`<h2 class="mono">${esc(id.slice(0, 12))}…</h2>
      <p style="margin:6px 0 12px">${pillFor(ex.status)} <span class="muted">${esc(ex.request || "")}</span></p>
      <pre class="out">${esc(JSON.stringify(d, null, 2).slice(0, 4000))}</pre>
      <div class="row" style="margin-top:14px">
        ${waiting && step != null && step >= 0 ? `
          <button id="ap-yes">Approve step ${step}</button>
          <button id="ap-no" class="ghost">Reject</button>
          <button id="ap-resume" class="ghost">Resume</button>` : ""}
        <button class="ghost" onclick="closeModal()">Close</button>
      </div>`);
    const ay = $("#ap-yes"), an = $("#ap-no"), ar = $("#ap-resume");
    if (ay) ay.onclick = () => decide(id, step, true);
    if (an) an.onclick = () => decide(id, step, false);
    if (ar) ar.onclick = async () => {
      try {
        const r = await api("/api/resume", { method: "POST",
          body: JSON.stringify({ execution_id: id, auto_approve: $("#eauto")?.checked || false }) });
        toast(`Resumed: ${r.status || "ok"}`);
        closeModal(); route();
      } catch (e) { toast(e.message); }
    };
  } catch (e) { openModal(`<p class="muted">${esc(e.message)}</p>`); }
}

async function decide(id, step, ok) {
  try {
    await api("/api/approve", { method: "POST",
      body: JSON.stringify({ execution_id: id, step, approve: ok, by: "dashboard" }) });
    toast(ok ? "Step approved" : "Step rejected");
    closeModal(); route();
  } catch (e) { toast(e.message); }
}

RENDER["engine$mount"] = () => {
  $$("#ehist .result-row").forEach((tr) => {
    tr.onclick = () => inspectExecution(tr.dataset.id);
  });
  const showRun = (d) => {
    $("#eres").style.display = "";
    $("#ebody").innerHTML = `<pre class="out">${esc(JSON.stringify(d, null, 2).slice(0, 6000))}</pre>`;
    const acts = $("#eactions");
    const id = d.execution_id;
    const waiting = id && (d.status === "WAITING_APPROVAL" || d.status === "PENDING");
    acts.innerHTML = id
      ? `<button class="ghost" id="e-inspect">Inspect ${esc(String(id).slice(0, 8))}…</button>
         ${waiting ? `<span class="muted" style="font-size:13px">waiting — inspect to approve steps</span>` : ""}`
      : "";
    const b = $("#e-inspect");
    if (b) b.onclick = () => inspectExecution(id);
  };
  const showPretty = (kind, d) => {
    $("#eres").style.display = "";
    $("#eactions").innerHTML = "";
    const body = $("#ebody");
    if (kind === "resolve" && d.candidates) {
      body.innerHTML = `<p class="muted" style="font-size:13px;margin-bottom:10px">intent: <b>${esc((d.intent && d.intent.intent) || "unknown")}</b></p>
        <table><thead><tr><th>#</th><th>Name</th><th>Type</th><th>Score</th><th>Risk</th></tr></thead><tbody>` +
        d.candidates.slice(0, 12).map((c, i) =>
          `<tr><td class="muted">${i + 1}</td><td class="mono">${esc(c.name)}</td>
           <td>${esc(c.definition_type || "")}</td><td>${esc(c.score)}</td><td>${esc(c.risk || "")}</td></tr>`).join("") +
        `</tbody></table>`;
    } else if (kind === "plan" && d.steps) {
      body.innerHTML = `<pre class="out">${esc(d.steps.map((s) => `${s.index}. [${s.decision || "allowed"}] ${s.description}`).join("\n"))}</pre>`;
    } else {
      body.innerHTML = `<pre class="out">${esc(JSON.stringify(d, null, 2).slice(0, 6000))}</pre>`;
    }
  };
  const ask = async (kind, btn) => {
    const q = $("#eq").value.trim();
    if (!q) { toast("Type a request first"); return; }
    setBusy(btn, true);
    try {
      const exec = $("#eexec").checked, auto = $("#eauto").checked;
      if (kind === "run" && exec && !confirm("Execute for real (not a dry-run)?")) return;
      const url = kind === "resolve" ? "/api/resolve" : kind === "plan" ? "/api/plan" : "/api/run";
      const d = await api(url, { method: "POST",
        body: JSON.stringify({ request: q, dry_run: !(kind === "run" && exec), auto_approve: auto }) });
      if (kind === "run") showRun(d);
      else { $("#eres").style.display = ""; $("#eactions").innerHTML = ""; $("#epre").textContent = JSON.stringify(d, null, 2).slice(0, 6000); }
    } catch (e) { toast(e.message); } finally { setBusy(btn, false); }
  };
  $("#eb1").onclick = (e) => ask("resolve", e.target);
  $("#eb2").onclick = (e) => ask("plan", e.target);
  $("#eb3").onclick = (e) => ask("run", e.target);
};

/* ---------------- install ---------------- */
RENDER.install = async () => {
  const plats = await api("/api/platforms").catch(() => []);
  const opts = plats.map((p) => `<option value="${p.id}">${esc(p.id)}</option>`).join("");
  return `
  <h1>Install</h1>
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

/* ---------------- tools ---------------- */
RENDER.tools = async () => {
  const [tele, wfs] = await Promise.all([
    api("/api/telemetry").catch(() => null),
    api("/api/workflows").catch(() => ({})),
  ]);
  const wfList = wfs.workflows || wfs.ids || [];
  const wfRows = (Array.isArray(wfList) ? wfList : []).map((w) => {
    const id = typeof w === "string" ? w : (w.id || w.name || "");
    return `<tr><td class="mono">${esc(id)}</td>
      <td class="row" style="gap:6px"><button class="ghost" data-wf="${esc(id)}" data-act="validate">Validate</button>
      <button class="ghost" data-wf="${esc(id)}" data-act="run">Dry-run</button></td></tr>`;
  }).join("");
  return `
  <h1>Tools</h1>
  <p class="lede">Delegation, versions, telemetry, workflows.</p>
  <div class="panel"><h3>Delegate sub-agents</h3><div class="row">
    <input type="text" id="t-agent" placeholder="agent name">
    <button id="t-delegate" class="ghost">Resolve</button><span id="t-del-out" class="muted"></span>
  </div></div>
  <div class="panel"><h3>Resolve version</h3><div class="row">
    <input type="text" id="t-spec" placeholder="e.g. terraform-infrastructure@^1.0">
    <button id="t-ver" class="ghost">Resolve</button><span id="t-ver-out" class="muted"></span>
  </div></div>
  <div class="panel"><h3>Who uses a tool?</h3><div class="row">
    <input type="text" id="t-tool" placeholder="e.g. Bash, kubectl, terraform">
    <button id="t-cap" class="ghost">Lookup</button>
  </div><div id="t-cap-out" style="margin-top:10px"></div></div>
  <div class="panel"><h3>Telemetry</h3>
    <pre class="out">${esc(JSON.stringify(tele || { tracked: 0 }, null, 2).slice(0, 1200))}</pre></div>
  <div class="panel"><h3>Workflows</h3>
    <table><thead><tr><th>ID</th><th>Actions</th></tr></thead><tbody id="wrows">
    ${wfRows || `<tr><td colspan="2" class="muted">No workflows found.</td></tr>`}</tbody></table>
    <pre class="out" id="wout" style="display:none;margin-top:12px"></pre></div>`;
};

RENDER["tools$mount"] = () => {
  $("#t-delegate").onclick = async () => {
    const a = $("#t-agent").value.trim();
    if (!a) return;
    try {
      const d = await api("/api/delegate?agent=" + encodeURIComponent(a), { method: "POST" });
      $("#t-del-out").textContent = d.delegated
        ? `${d.succeeded}/${d.total} sub-agents ok (${d.pattern})` : (d.reason || "no delegation");
    } catch (e) { toast(e.message); }
  };
  $("#t-ver").onclick = async () => {
    const s = $("#t-spec").value.trim();
    if (!s) return;
    try {
      const d = await api("/api/resolve-version?spec=" + encodeURIComponent(s));
      $("#t-ver-out").textContent = d.resolved;
    } catch (e) { toast(e.message); }
  };
  $("#t-cap").onclick = async () => {
    const t = $("#t-tool").value.trim();
    if (!t) return;
    const box = $("#t-cap-out");
    box.innerHTML = `<p class="muted">Looking up…</p>`;
    try {
      const d = await api("/api/capabilities?tool=" + encodeURIComponent(t));
      box.innerHTML = d.length
        ? `<table><thead><tr><th>Definition</th><th>Capability</th></tr></thead><tbody>` +
          d.slice(0, 20).map((r) => `<tr><td class="mono">${esc(r.definition)}</td><td>${esc(r.capability)}</td></tr>`).join("") +
          `</tbody></table>`
        : `<p class="muted">No definitions invoke ‘${esc(t)}’.</p>`;
    } catch (e) { box.innerHTML = `<p class="muted">${esc(e.message)}</p>`; }
  };
  $$("#wrows button").forEach((b) => {
    b.onclick = async () => {
      const out = $("#wout"); out.style.display = "";
      out.textContent = "Working…";
      try {
        const d = await api("/api/workflows/" + b.dataset.act, { method: "POST",
          body: JSON.stringify({ workflow_id: b.dataset.wf, execute: false }) });
        out.textContent = JSON.stringify(d, null, 2).slice(0, 4000);
      } catch (e) { out.textContent = e.message; }
    };
  });
};

/* ---------------- boot ---------------- */
async function ensureCatalog() {
  try {
    const h = await api("/api/health");
    if (h.catalog_ok) return true;
    $("#setup-msg").textContent =
      `No catalog found at ${h.root || "this location"}. Paste the path to your Kdesk-Catalog checkout.`;
  } catch (e) {
    $("#setup-msg").textContent = "Server unreachable. Is `kdesk serve` running?";
  }
  $("#splash").classList.add("done");
  $("#setup").classList.add("show");
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
