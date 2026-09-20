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
  main.innerHTML = `<div class="page"><p class="muted">Loading…</p></div>`;
  try {
    main.innerHTML = `<div class="page">${await RENDER[page]()}</div>`;
    if (RENDER[page + "$mount"]) RENDER[page + "$mount"]();
  } catch (e) {
    main.innerHTML = `<div class="page"><h1>Something broke</h1>
      <p class="lede">${esc(e.message)}</p>
      <button class="ghost" onclick="location.reload()">Retry</button></div>`;
  }
  $("#main").scrollTop = 0;
}
window.addEventListener("hashchange", route);

/* ---------------- dashboard ---------------- */
RENDER.dashboard = async () => {
  const [stats, verify] = await Promise.all([
    api("/api/stats?fast=true"),
    api("/api/verify?fast=true").catch(() => null),
  ]);
  const cards = [
    [stats.definitions_total ?? stats.total_files ?? "—", "definitions"],
    [stats.agents ?? "—", "agents"],
    [stats.skills ?? "—", "skills"],
    [stats.platforms ?? "—", "platforms"],
    [stats.workflows ?? "—", "workflows"],
    [stats.platform_output_files ?? "—", "generated files"],
  ];
  const v = verify
    ? pillFor(verify.status) + ` <span class="muted">${verify.checks ? "" : ""}</span>`
    : `<span class="pill warn">UNKNOWN</span>`;
  return `
    <h1>Dashboard</h1>
    <p class="lede">Catalog health at a glance &nbsp;${v}</p>
    <div class="grid">${cards.map(([n, l]) =>
      `<div class="card"><div class="stat-num">${n}</div><div class="stat-label">${l}</div></div>`).join("")}
    </div>
    <div class="panel" style="margin-top:16px">
      <h3>Start here</h3>
      <div class="row">
        <button class="ghost" onclick="location.hash='#/catalog'">Browse catalog</button>
        <button class="ghost" onclick="location.hash='#/quality'">Run quality gates</button>
        <button class="ghost" onclick="location.hash='#/doctor'">Diagnose a project</button>
        <button class="ghost" onclick="location.hash='#/converter'">Convert to a platform</button>
      </div>
    </div>`;
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
  </div>
  <div class="panel" id="results"><p class="muted">Type to search.</p></div>`;

RENDER["catalog$mount"] = () => {
  const q = $("#q"), box = $("#results");
  const run = async () => {
    const term = q.value.trim();
    if (!term) return;
    box.innerHTML = `<p class="muted">Searching…</p>`;
    try {
      catalogCache = await api("/api/search?q=" + encodeURIComponent(term));
      if (!catalogCache.length) { box.innerHTML = `<p class="muted">No results.</p>`; return; }
      box.innerHTML = `<table><thead><tr><th>Type</th><th>Name</th><th>Category</th></tr></thead>
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
  setTimeout(() => q.focus(), 100);
};

async function showDefinition(h) {
  openModal(`<p class="muted">Loading…</p>`);
  try {
    const d = await api(`/api/definition/${h.type}/${encodeURIComponent(h.name)}`);
    const caps = (d.capabilities || []).map((c) =>
      `<tr><td class="mono">${esc(c.name || "")}</td><td>${esc(c.description || "")}</td></tr>`).join("");
    openModal(`
      <h2 class="mono">${esc(d.name || h.name)}</h2>
      <p class="muted">${esc(d.display_name || "")} · v${esc(d.version || "?")} · ${esc(d.category || "")}</p>
      <p style="margin:12px 0">${esc(d.description || "")}</p>
      ${caps ? `<table><thead><tr><th>Capability</th><th>Description</th></tr></thead><tbody>${caps}</tbody></table>` : ""}
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
  <p class="lede">Every gate, live. Click a card for raw output.</p>
  <div class="grid" id="gates"><div class="card"><p class="muted">Running gates…</p></div></div>`;

RENDER["quality$mount"] = async () => {
  const grid = $("#gates");
  const results = await Promise.all(GATES.map(async ([id, label, url, fmt]) => {
    try {
      const d = await api(url);
      const [st, sub] = fmt(d);
      return { id, label, st, sub, raw: d };
    } catch (e) { return { id, label, st: "ERROR", sub: e.message, raw: { error: e.message } }; }
  }));
  window._gates = Object.fromEntries(results.map((r) => [r.id, r.raw]));
  grid.innerHTML = results.map((r, i) => `
    <div class="card result-row" data-id="${r.id}" style="animation-delay:${0.05 * i}s">
      <div>${pillFor(r.st)}</div>
      <div style="font-weight:700;margin:8px 0 2px">${r.label}</div>
      <div class="muted" style="font-size:13px">${esc(r.sub)}</div>
    </div>`).join("");
  $$(".result-row", grid).forEach((c) => {
    c.onclick = () => openModal(`<h2>${esc(c.dataset.id)}</h2>
      <pre class="out" style="margin-top:12px">${esc(JSON.stringify(window._gates[c.dataset.id], null, 2).slice(0, 6000))}</pre>
      <div class="row" style="margin-top:14px"><button class="ghost" onclick="closeModal()">Close</button></div>`);
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
        <option value="diagnose">diagnose</option><option value="fix">fix (dry-run)</option>
      </select>
      <input type="text" id="droot" placeholder="Project path (blank = this repo)">
      <button id="dbtn">Run</button>
    </div>
  </div>
  <div class="panel" id="dres" style="display:none"><h3>Report</h3><div id="dbody"></div></div>`;
};

RENDER["doctor$mount"] = () => {
  $("#dbtn").onclick = async (e) => {
    const b = e.target; setBusy(b, true, "Diagnosing…");
    try {
      const d = await api("/api/doctor", { method: "POST", body: JSON.stringify({
        platform: $("#dplat").value, mode: $("#dmode").value,
        project_root: $("#droot").value.trim() || null, dry_run: true,
      }) });
      const box = $("#dres"); box.style.display = "";
      const rep = d.report || d;
      const score = rep.score != null ? rep.score : 100;
      const C = 2 * Math.PI * 34;
      const issues = (rep.issues || []).slice(0, 60);
      $("#dbody").innerHTML = `
        <div class="ring">
          <svg width="88" height="88"><circle class="bg" cx="44" cy="44" r="34" fill="none" stroke-width="9"/>
          <circle class="fg" cx="44" cy="44" r="34" fill="none" stroke-width="9"
            stroke-dasharray="${C}" stroke-dashoffset="${C}"/></svg>
          <div><div class="pct">${score}%</div><div class="muted">health · ${esc(rep.platform || "")}</div></div>
        </div>
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
};

/* ---------------- engine ---------------- */
RENDER.engine = async () => {
  const h = await api("/api/history?limit=8").catch(() => []);
  const rows = (h || []).map((x) =>
    `<tr><td class="mono">${esc((x.execution_id || "").slice(0, 12))}</td>
     <td>${esc(x.request || "")}</td><td>${pillFor(x.status)}</td></tr>`).join("");
  return `
  <h1>Engine</h1>
  <p class="lede">Resolve intent, plan, and dry-run executions.</p>
  <div class="panel"><h3>Ask</h3>
    <div class="row"><input type="text" id="eq" placeholder="e.g. lint my terraform code">
      <button id="eb1">Resolve</button><button id="eb2" class="ghost">Plan</button>
      <button id="eb3" class="ghost">Dry-run</button></div>
  </div>
  <div class="panel" id="eres" style="display:none"><h3>Result</h3><pre class="out" id="epre"></pre></div>
  <div class="panel"><h3>Recent executions</h3>
    <table><thead><tr><th>ID</th><th>Request</th><th>Status</th></tr></thead><tbody>${rows || `<tr><td colspan="3" class="muted">None yet.</td></tr>`}</tbody></table></div>`;
};

RENDER["engine$mount"] = () => {
  const ask = async (kind, btn) => {
    const q = $("#eq").value.trim();
    if (!q) { toast("Type a request first"); return; }
    setBusy(btn, true);
    try {
      const url = kind === "resolve" ? "/api/resolve" : kind === "plan" ? "/api/plan" : "/api/run";
      const d = await api(url, { method: "POST", body: JSON.stringify({ request: q, dry_run: true }) });
      $("#eres").style.display = "";
      $("#epre").textContent = JSON.stringify(d, null, 2).slice(0, 6000);
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
  <p class="lede">Dry-run installs and drift checks. Nothing touches disk unless dry-run is off.</p>
  <div class="panel"><div class="row">
    <select id="iplat">${opts}</select>
    <input type="text" id="iscope" placeholder="scope (optional)" style="max-width:160px">
    <input type="text" id="itool" placeholder="tool (optional)" style="max-width:160px">
    <label class="muted" style="font-size:13px"><input type="checkbox" id="idry" checked> dry-run</label>
    <button id="ibtn">Install</button><button id="dbtn2" class="ghost">Drift</button>
  </div></div>
  <div class="panel" id="ires" style="display:none"><h3>Result</h3><pre class="out" id="ipre"></pre></div>`;
};

RENDER["install$mount"] = () => {
  const show = (d) => {
    $("#ires").style.display = "";
    $("#ipre").textContent = JSON.stringify(d, null, 2).slice(0, 5000);
  };
  $("#ibtn").onclick = async (e) => {
    const b = e.target; setBusy(b, true, "Installing…");
    try {
      show(await api("/api/install", { method: "POST", body: JSON.stringify({
        platform: $("#iplat").value,
        scope: $("#iscope").value.trim() || null,
        tool: $("#itool").value.trim() || null,
        dry_run: $("#idry").checked,
      }) }));
    } catch (err) { toast(err.message); } finally { setBusy(b, false); }
  };
  $("#dbtn2").onclick = async () => {
    try {
      show(await api("/api/drift?platform=" + encodeURIComponent($("#iplat").value)));
    } catch (err) { toast(err.message); }
  };
};

/* ---------------- boot ---------------- */
(async function boot() {
  await bootIdentity();
  if (!location.hash) location.hash = "#/dashboard";
  route();
})();
