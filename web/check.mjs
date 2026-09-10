import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {Chess} from './dist/chess.mjs';

const game=new Chess();
assert.equal(game.moves().length,20);
assert.throws(()=>game.move({from:'e2',to:'e5'}));
assert.equal(game.history().length,0);
for(const move of ['f3','e5','g4','Qh4#']) game.move(move);
assert.equal(game.isCheckmate(),true);
game.undo();assert.equal(game.isGameOver(),false);
game.reset();
for(const move of ['e4','a6','e5','d5','exd6'])game.move(move);
assert.equal(game.get('d5'),undefined);assert.equal(game.get('d6').color,'w');
game.reset();
for(const move of ['e4','e5','Nf3','Nc6','Bc4','Nf6','O-O'])game.move(move);
assert.equal(game.get('g1').type,'k');assert.equal(game.get('f1').type,'r');
for(const promotion of ['q','r','b','n']) {
  const position=new Chess('7k/P7/8/8/8/8/8/7K w - - 0 1');
  position.move({from:'a7',to:'a8',promotion});assert.equal(position.get('a8').type,promotion);
}
assert.equal(new Chess('7k/5K2/6Q1/8/8/8/8/8 b - - 0 1').isStalemate(),true);
assert.equal(new Chess('7k/8/8/8/8/8/8/7K w - - 0 1').isInsufficientMaterial(),true);
game.reset();for(const move of ['Nf3','Nf6','Ng1','Ng8','Nf3','Nf6','Ng1','Ng8'])game.move(move);
assert.equal(game.isThreefoldRepetition(),true);
assert.equal(new Chess('7k/8/8/8/8/8/R7/7K w - - 100 51').isDrawByFiftyMoves(),true);
for(const color of ['w','b'])for(const type of ['p','n','b','r','q','k'])assert.ok(existsSync(`dist/assets/${color}${type}.png`));
const html=readFileSync('dist/index.html','utf8');
for(const match of html.matchAll(/(?:src|href)="([^"#]+)"/g))if(match[1]!=='./')assert.ok(existsSync(`dist/${match[1]}`),`Missing asset: ${match[1]}`);
console.log('PASS: legal moves, illegal-move rejection, checkmate, undo, castling, en passant, four promotions, stalemate, material/repetition/50-move draws, and local assets.');
