// Exercise the actual browser transport against a running Python server.
import assert from 'node:assert/strict';
import {RoomClient} from './dist/online.mjs';
const baseUrl=process.argv[2]||'http://127.0.0.1:8766';
const storage=()=>{const values=new Map();return {getItem:key=>values.get(key),setItem:(key,value)=>values.set(key,value)};};
const whiteStore=storage(),blackStore=storage();
const white=new RoomClient({baseUrl,storage:whiteStore});
const black=new RoomClient({baseUrl,storage:blackStore});
const reconnected=new RoomClient({baseUrl,storage:blackStore});
try {
  const room=await white.create();
  assert.equal(room.color,'w');assert.equal(room.ready,false);
  await black.join(room.room);
  await white.sync();
  assert.equal(black.state.color,'b');assert.equal(white.state.ready,true);
  await assert.rejects(()=>black.move('e7e5'),/other player's turn/);
  await assert.rejects(()=>white.move('e2e5'),/not legal/);
  await white.move('e2e4');
  // Let the normal polling path deliver the opponent's move.
  const deadline=Date.now()+5000;
  while(black.state.moves.length<1&&Date.now()<deadline)await new Promise(resolve=>setTimeout(resolve,100));
  assert.deepEqual(black.state.moves,['e2e4']);
  await black.move('e7e5');await white.sync();
  assert.equal(white.state.fen,black.state.fen);
  black.stop();await reconnected.resume(room.room);
  assert.equal(reconnected.state.color,'b');assert.deepEqual(reconnected.state.moves,['e2e4','e7e5']);
  assert.equal(reconnected.state.fen,white.state.fen);
  console.log('PASS: two independent browser clients, room invitation, turn/illegal-move rejection, automatic polling, identical boards, and saved-seat reconnection.');
} finally {white.stop();black.stop();reconnected.stop();}
