import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { once } from 'node:events';
import { createChessServer } from './server.mjs';

test('two-player rooms validate, synchronize and persist moves', async t => {
  const dataDir = mkdtempSync(join(tmpdir(), 'chess-test-'));
  let server, base;
  async function start() {
    server = createChessServer({ dataDir });
    server.listen(0, '127.0.0.1');
    await once(server, 'listening');
    base = `http://127.0.0.1:${server.address().port}`;
  }
  async function stop() { await new Promise(resolve => server.close(resolve)); }
  await start();
  t.after(stop);
  async function api(path, body, token, status = 200) {
    const response = await fetch(base + path, {
      method: body === undefined ? 'GET' : 'POST',
      headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
      body: body === undefined ? undefined : JSON.stringify(body)
    });
    const result = await response.json();
    assert.equal(response.status, status, JSON.stringify(result));
    return result;
  }
  const path = '/api/rooms/01234';
  const white = await api(path + '/join', {});
  assert.equal(white.color, 'w');
  assert.equal(white.ready, false);
  await api(path + '/moves', { from: 'e2', to: 'e4', version: 0 }, white.token, 409);
  const black = await api(path + '/join', {});
  assert.equal(black.color, 'b');
  assert.equal(black.ready, true);
  await api(path + '/join', {}, undefined, 409);
  await api(path, undefined, undefined, 401);
  await api(path, undefined, 'fake-token', 401);
  const resumed = await api(path + '/join', {}, white.token);
  assert.equal(resumed.color, 'w');
  assert.equal(resumed.token, undefined);
  const move = { from: 'e2', to: 'e4', version: resumed.version };
  await api(path + '/moves', move, black.token, 403);
  await api(path + '/moves', { ...move, to: 'e5' }, white.token, 400);
  const concurrent = await Promise.all([0, 1].map(() => fetch(base + path + '/moves', {
    method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${white.token}` }, body: JSON.stringify(move)
  })));
  assert.deepEqual(concurrent.map(response => response.status).sort(), [200, 409]);
  const afterWhite = await api(path, undefined, black.token);
  assert.deepEqual(afterWhite.moves, ['e4']);
  const afterBlack = await api(path + '/moves', { from: 'e7', to: 'e5', version: afterWhite.version }, black.token);
  assert.deepEqual(afterBlack.moves, ['e4', 'e5']);
  assert.deepEqual((await api(path, undefined, white.token)).moves, afterBlack.moves);
  const other = await api('/api/rooms/99999/join', {});
  assert.deepEqual(other.moves, []);
  await api('/api/rooms/99999', undefined, white.token, 401);
  await api('/api/rooms/1234/join', {}, undefined, 404);
  for (const asset of ['/', '/app.js', '/chess.js', '/assets/wk.png']) {
    const response = await fetch(base + asset);
    assert.equal(response.status, 200);
    if (asset.endsWith('.js')) assert.match(response.headers.get('content-type'), /javascript/);
  }
  assert.equal((await fetch(base + '/data/chess.sqlite')).status, 404);
  assert.equal((await fetch(base + path + '/join', { method: 'POST', headers: { Origin: 'https://other.example' }, body: '{}' })).status, 403);
  await stop();
  await start();
  const persisted = await api(path, undefined, white.token);
  assert.deepEqual(persisted.moves, ['e4', 'e5']);
  assert.equal(persisted.version, afterBlack.version);
  assert.equal((await api(path + '/join', {}, black.token)).color, 'b');

  // A complete game remains final; moves cannot continue after checkmate.
  const endPath = '/api/rooms/54321';
  const w = await api(endPath + '/join', {});
  const b = await api(endPath + '/join', {});
  let version = b.version;
  for (const [from, to, token] of [['f2','f3',w.token],['e7','e5',b.token],['g2','g4',w.token],['d8','h4',b.token]]) {
    version = (await api(endPath + '/moves', { from, to, version }, token)).version;
  }
  await api(endPath + '/moves', { from: 'e2', to: 'e4', version }, w.token, 409);
});
