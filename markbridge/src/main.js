const { app, BrowserWindow, ipcMain, dialog, Tray, Menu, nativeImage, shell } = require('electron')
const path  = require('path')
const fs    = require('fs')
const { spawn } = require('child_process')

// ── Config ────────────────────────────────────────────────────────────────────
const SUPPORTED = new Set(['.pdf','.docx','.pptx','.xlsx','.xls','.html','.htm',
                            '.csv','.json','.xml','.epub','.msg'])

let win, tray, pyProc
let pendingResolves = new Map()
let msgId = 0

// ── Python worker ─────────────────────────────────────────────────────────────
function pythonExe() {
  const candidates = process.platform === 'win32'
    ? ['python', 'python3', 'py']
    : ['python3', 'python']
  return candidates[0]
}

function pythonScript() {
  // In packaged app, python/ is in resources/python/
  const packed = path.join(process.resourcesPath || '', 'python', 'convert.py')
  if (fs.existsSync(packed)) return packed
  return path.join(__dirname, '..', 'python', 'convert.py')
}

function startPython() {
  const script = pythonScript()
  pyProc = spawn(pythonExe(), [script], { stdio: ['pipe','pipe','pipe'] })

  pyProc.stdout.on('data', data => {
    String(data).split('\n').forEach(line => {
      if (!line.trim()) return
      try {
        const msg = JSON.parse(line)
        const resolve = pendingResolves.get(msg._id)
        if (resolve) { pendingResolves.delete(msg._id); resolve(msg) }
        else win?.webContents.send('py-event', msg)
      } catch {}
    })
  })

  pyProc.stderr.on('data', d => win?.webContents.send('log', { level:'err', msg: String(d).trim() }))

  pyProc.on('exit', code => {
    win?.webContents.send('log', { level:'warn', msg: `Python worker exited (${code})` })
  })
}

function pyCall(req) {
  return new Promise((resolve, reject) => {
    if (!pyProc || pyProc.exitCode !== null) {
      reject(new Error('Python worker not running')); return
    }
    const id = ++msgId
    req._id = id
    pendingResolves.set(id, resolve)
    setTimeout(() => { pendingResolves.delete(id); reject(new Error('Timeout')) }, 30000)
    pyProc.stdin.write(JSON.stringify(req) + '\n')
  })
}

// ── Window ────────────────────────────────────────────────────────────────────
function createWindow() {
  win = new BrowserWindow({
    width: 960, height: 640,
    minWidth: 720, minHeight: 480,
    frame: false,
    transparent: false,
    backgroundColor: '#0D0D1A',
    icon: path.join(__dirname, '..', 'assets', 'icon.png'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    }
  })
  win.loadFile(path.join(__dirname, 'index.html'))
  win.on('close', e => { e.preventDefault(); win.hide() })
}

// ── Tray ──────────────────────────────────────────────────────────────────────
function createTray() {
  const iconPath = path.join(__dirname, '..', 'assets', 'tray.png')
  const img = fs.existsSync(iconPath)
    ? nativeImage.createFromPath(iconPath)
    : nativeImage.createEmpty()
  tray = new Tray(img)
  tray.setToolTip('MarkBridge')
  tray.setContextMenu(Menu.buildFromTemplate([
    { label: 'Mostrar MarkBridge', click: () => { win.show(); win.focus() } },
    { type: 'separator' },
    { label: 'Sair', click: () => { app.exit(0) } }
  ]))
  tray.on('double-click', () => { win.show(); win.focus() })
}

// ── IPC handlers ──────────────────────────────────────────────────────────────
ipcMain.handle('ping-python', async () => {
  try { return await pyCall({ action: 'ping' }) }
  catch (e) { return { ok: false, error: e.message } }
})

ipcMain.handle('convert', async (_e, req) => {
  try { return await pyCall({ action: 'convert', ...req }) }
  catch (e) { return { ok: false, error: e.message } }
})

ipcMain.handle('pick-files', async () => {
  const { canceled, filePaths } = await dialog.showOpenDialog(win, {
    properties: ['openFile', 'multiSelections'],
    filters: [
      { name: 'Documentos', extensions: ['pdf','docx','pptx','xlsx','xls','html','htm','csv','json','xml'] },
      { name: 'Todos',      extensions: ['*'] }
    ]
  })
  return canceled ? [] : filePaths
})

ipcMain.handle('pick-folder', async () => {
  const { canceled, filePaths } = await dialog.showOpenDialog(win, {
    properties: ['openDirectory', 'createDirectory']
  })
  return canceled ? null : filePaths[0]
})

ipcMain.handle('open-folder', (_e, p) => { shell.openPath(p) })
ipcMain.handle('win-minimize', ()  => win.minimize())
ipcMain.handle('win-close',   ()  => win.hide())

// ── File drop via webContents ─────────────────────────────────────────────────
app.on('web-contents-created', (_e, contents) => {
  contents.on('will-navigate', e => e.preventDefault())
})

// ── App lifecycle ─────────────────────────────────────────────────────────────
app.whenReady().then(() => {
  createWindow()
  createTray()
  startPython()
})

app.on('window-all-closed', e => e.preventDefault()) // keep in tray
app.on('before-quit', () => { pyProc?.kill(); })
