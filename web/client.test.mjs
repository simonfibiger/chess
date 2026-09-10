import { parseHTML } from 'linkedom';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import { readFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { once } from 'node:events';
import { Chess } from './dist/chess.js';
import { createChessServer } from './server.mjs';

const root = new URL('.', import.meta.url);
const server = createChessServer({ dataDir: mkdtempSync(join(tmpdir(), 'chess-ui-')) });
server.listen(0, '127.0.0.1');
await once(server, 'listening');
const base = `http://127.0.0.1:${server.address().port}`;
function client(saved = new Map()) {
  const { window, document } = parseHTML(readFileSync(new URL('dist/index.html', root), 'utf8'));
  window.confirm = () => true;
  const context = vm.createContext({ document, window, Chess, console, AbortController, AbortSignal,
    fetch: (path, options) => fetch(base + path, options),
    localStorage: { getItem: key => saved.get(key) || null, setItem: (key, value) => saved.set(key, value), removeItem: key => saved.delete(key) },
    setInterval: () => 1, clearInterval: () => {} });
  vm.runInContext(readFileSync(new URL('dist/app.js', root), 'utf8').replace("import { Chess } from './chess.js';", ''), context);
  return { document, saved, run: code => vm.runInContext(code, context) };
}
try {
  const white = client();
  assert.equal(white.document.querySelectorAll('.square').length, 64);
  assert.equal(white.document.querySelectorAll('.square img').length, 32);
  white.document.querySelector('[data-square=e2]').onclick();
  assert.equal(white.document.querySelectorAll('.legal').length, 2);
  white.document.querySelector('[data-square=e4]').onclick();
  assert.equal(white.run('game.history().join()'), 'e4');
  white.document.getElementById('undo').onclick();
  assert.equal(white.run('game.history().length'), 0);
  await white.run("joinRoom('12345')");
  assert.equal(white.run('room.color'), 'w');
  assert.equal(white.document.getElementById('undo').disabled, true);
  const black = client();
  await black.run("joinRoom('12345')");
  assert.equal(black.run('room.color'), 'b');
  assert.equal(black.run('flipped'), true);
  await white.run('syncRoom()');
  await black.run("makeMove('e7','e5')");
  assert.equal(black.run('game.history().length'), 0);
  await white.run("makeMove('e2','e4')");
  await black.run('syncRoom()');
  assert.equal(black.run('game.history().join()'), 'e4');
  await black.run("makeMove('e7','e5')");
  await white.run('syncRoom()');
  assert.equal(white.run('game.history().join()'), 'e4,e5');
  white.document.getElementById('leave-room').onclick();
  await white.run("joinRoom('12345')");
  assert.equal(white.run('game.history().join()'), 'e4,e5');
  assert.equal(white.run('room.color'), 'w');
  const third = client();
  await third.run("joinRoom('12345')");
  assert.equal(third.run('room'), null);
  assert.match(third.document.getElementById('room-message').textContent, /two players/);
  console.log('PASS: DOM renders 64 squares and 32 pieces; click/select/move/undo; two clients join, enforce turns, sync both ways, restore seats, reject a third player.');
} finally { await new Promise(resolve => server.close(resolve)); }
