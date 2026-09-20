'use strict';
/* Kdesk Catalog VS Code extension — thin client over `python -m kdesk.cli`. */
const vscode = require('vscode');
const cp = require('child_process');

let output;

function cfg() {
  return vscode.workspace.getConfiguration('kdesk');
}

function repoRoot() {
  const custom = (cfg().get('repoRoot') || '').trim();
  if (custom) return custom;
  const folders = vscode.workspace.workspaceFolders;
  if (folders && folders.length) return folders[0].uri.fsPath;
  return '';
}

function runCli(args, opts) {
  const python = cfg().get('pythonPath') || 'python';
  const root = repoRoot();
  return new Promise((resolve) => {
    const full = ['-m', 'kdesk.cli', '--root', root].concat(args);
    output.appendLine(`$ ${python} ${full.join(' ')}`);
    const proc = cp.spawn(python, full, Object.assign({ cwd: root || undefined }, opts || {}));
    let stdout = '', stderr = '';
    proc.stdout.on('data', (d) => { stdout += d.toString(); });
    proc.stderr.on('data', (d) => { stderr += d.toString(); });
    proc.on('error', (e) => resolve({ code: 127, stdout, stderr: String(e) }));
    proc.on('close', (code) => resolve({ code: code == null ? 1 : code, stdout, stderr }));
  });
}

function parseJson(stdout) {
  try { return JSON.parse(stdout); } catch (e) { return null; }
}

async function cmdSearch() {
  const query = await vscode.window.showInputBox({
    prompt: 'Search 3,093 agents & skills',
    placeHolder: 'e.g. kubernetes, terraform, testing',
  });
  if (!query) return;
  await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: `Kdesk: searching “${query}”…` },
    async () => {
      const { code, stdout, stderr } = await runCli(['registry', '--search', query]);
      if (code !== 0) {
        vscode.window.showErrorMessage(`Kdesk search failed: ${stderr.slice(0, 300)}`);
        return;
      }
      const lines = stdout.split('\n').map((l) => l.trim()).filter(Boolean);
      if (!lines.length) {
        vscode.window.showInformationMessage(`Kdesk: no results for “${query}”.`);
        return;
      }
      const pick = await vscode.window.showQuickPick(
        lines.slice(0, 50).map((l) => ({ label: l })),
        { placeHolder: `${lines.length} result(s) — pick one to insert a reference` });
      if (pick) insertText(`\n> Kdesk: ${pick.label}\n`);
    });
}

async function cmdInsert() {
  const query = await vscode.window.showInputBox({
    prompt: 'Which agent/skill? (type part of the name)',
    placeHolder: 'e.g. auto-scaling',
  });
  if (!query) return;
  const { code, stdout } = await runCli(['registry', '--search', query]);
  if (code !== 0) { vscode.window.showErrorMessage('Kdesk search failed.'); return; }
  const lines = stdout.split('\n').map((l) => l.trim()).filter(Boolean);
  if (!lines.length) { vscode.window.showInformationMessage('No matches.'); return; }
  const pick = await vscode.window.showQuickPick(
    lines.slice(0, 50).map((l) => ({ label: l })));
  if (pick) insertText(`\n> Kdesk: ${pick.label}\n`);
}

function insertText(text) {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showWarningMessage('Kdesk: open a file first, then insert.');
    return;
  }
  editor.edit((b) => b.insert(editor.selection.active, text));
}

async function cmdDoctor() {
  const platform = await vscode.window.showQuickPick(
    ['claude_code', 'cursor', 'github_copilot', 'windsurf', 'opencode', 'codex_cli'],
    { placeHolder: 'Target platform for diagnosis' });
  if (!platform) return;
  output.show(true);
  output.appendLine(`Kdesk Doctor → ${platform} @ ${repoRoot() || '(workspace)'}`);
  await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: 'Kdesk Doctor running…' },
    async () => {
      const { code, stdout } = await runCli(
        ['doctor', '--mode', 'diagnose', '--platform', platform,
         '--project-root', repoRoot(), '--json']);
      const report = parseJson(stdout);
      if (report && report.report) {
        const r = report.report;
        output.appendLine(`Score: ${r.score}% — ${r.issues ? r.issues.length : 0} issue(s)`);
        vscode.window.showInformationMessage(
          `Kdesk Doctor: ${r.score}% health (${(r.issues || []).length} issues). See Output → Kdesk.`);
      } else {
        output.appendLine(stdout.slice(0, 2000));
        vscode.window.showWarningMessage(`Kdesk Doctor exited ${code}. See Output → Kdesk.`);
      }
    });
}

async function cmdStats() {
  const { code, stdout } = await runCli(['stats', '--fast']);
  const data = parseJson(stdout);
  if (code !== 0 || !data) { vscode.window.showErrorMessage('Kdesk stats failed.'); return; }
  vscode.window.showInformationMessage(
    `Kdesk: ${data.definitions_total} definitions (${data.agents} agents, ${data.skills} skills) · ${data.platforms} platforms`);
}

async function cmdConvert() {
  const { code, stdout } = await runCli(['adapters', '--format', 'json']);
  let platforms = [];
  try {
    const data = JSON.parse(stdout);
    platforms = (data.rows || []).map((r) => r.platform).filter(Boolean);
  } catch (e) { /* fall through */ }
  if (!platforms.length) {
    vscode.window.showErrorMessage('Kdesk: could not list platforms.');
    return;
  }
  const pick = await vscode.window.showQuickPick(platforms, {
    placeHolder: 'Convert catalog to…', canPickMany: true,
  });
  if (!pick || !pick.length) return;
  output.show(true);
  await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: 'Kdesk converting…' },
    async () => {
      const proc = cp.spawn(
        cfg().get('pythonPath') || 'python',
        ['scripts/universal-converter.py', '--platforms', pick.join(','), '--quiet'],
        { cwd: repoRoot() || undefined });
      proc.stdout.on('data', (d) => output.append(d.toString()));
      proc.stderr.on('data', (d) => output.append(d.toString()));
      await new Promise((res) => proc.on('close', res));
      vscode.window.showInformationMessage(`Kdesk: converted ${pick.length} platform(s). See platform-agents/.`);
    });
}

async function cmdDashboard() {
  const port = cfg().get('dashboardPort') || 8000;
  const url = `http://127.0.0.1:${port}/`;
  const open = await vscode.window.showQuickPick(
    [{ label: 'Open dashboard in browser', url },
     { label: 'Copy dashboard URL', url }],
    { placeHolder: 'Requires `kdesk serve` running' });
  if (!open) return;
  if (open.label.startsWith('Open')) vscode.env.openExternal(vscode.Uri.parse(url));
  else { await vscode.env.clipboard.writeText(url); vscode.window.showInformationMessage('Copied.'); }
}

/* Sidebar tree: top-level groups + quick actions */
class KdeskProvider {
  constructor() {
    this._emitter = new vscode.EventEmitter();
    this.onDidChangeTreeData = this._emitter.event;
    this._counts = null;
    this.refresh();
  }
  refresh() {
    runCli(['stats', '--fast']).then(({ stdout }) => {
      this._counts = parseJson(stdout) || {};
      this._emitter.fire();
    });
  }
  getTreeItem(el) { return el; }
  getChildren(el) {
    if (el) return Promise.resolve([]);
    const c = this._counts || {};
    const item = (label, desc, cmd) => {
      const it = new vscode.TreeItem(label, vscode.TreeItemCollapsibleState.None);
      it.description = desc;
      if (cmd) it.command = { command: cmd, title: label };
      it.iconPath = new vscode.ThemeIcon('symbol-misc');
      return it;
    };
    return Promise.resolve([
      item(`${c.definitions_total || '…'} definitions`, 'agents + skills', 'kdesk.search'),
      item(`${c.platforms || '…'} platforms`, 'conversion targets', 'kdesk.convert'),
      item('Diagnose project', 'doctor check', 'kdesk.doctor'),
      item('Open dashboard', 'local web UI', 'kdesk.dashboard'),
    ]);
  }
}

function activate(context) {
  output = vscode.window.createOutputChannel('Kdesk');
  context.subscriptions.push(
    vscode.commands.registerCommand('kdesk.search', cmdSearch),
    vscode.commands.registerCommand('kdesk.insert', cmdInsert),
    vscode.commands.registerCommand('kdesk.doctor', cmdDoctor),
    vscode.commands.registerCommand('kdesk.stats', cmdStats),
    vscode.commands.registerCommand('kdesk.convert', cmdConvert),
    vscode.commands.registerCommand('kdesk.dashboard', cmdDashboard),
    vscode.window.registerTreeDataProvider('kdesk-explorer', new KdeskProvider()),
    output,
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
