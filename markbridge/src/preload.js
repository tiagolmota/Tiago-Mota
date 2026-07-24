const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('mb', {
  pingPython:  ()       => ipcRenderer.invoke('ping-python'),
  convert:     req      => ipcRenderer.invoke('convert', req),
  pickFiles:   ()       => ipcRenderer.invoke('pick-files'),
  pickFolder:  ()       => ipcRenderer.invoke('pick-folder'),
  openFolder:  p        => ipcRenderer.invoke('open-folder', p),
  minimize:    ()       => ipcRenderer.invoke('win-minimize'),
  close:       ()       => ipcRenderer.invoke('win-close'),
  onLog:       cb       => ipcRenderer.on('log',      (_e, d) => cb(d)),
  onPyEvent:   cb       => ipcRenderer.on('py-event', (_e, d) => cb(d)),
})
