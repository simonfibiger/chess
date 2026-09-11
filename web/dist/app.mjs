import { Chess } from './chess.mjs';
import { RoomClient } from './online.mjs';

const game = new Chess();
const $ = (id) => document.getElementById(id);
const names = {p:'pawn',n:'knight',b:'bishop',r:'rook',q:'queen',k:'king'};
let selected = null, flipped = false, pendingPromotion = null, soundOn = false, audioContext;
let online=null, moveBusy=false, seenVersion=-1;
const colorName = (color) => color === 'w' ? 'White' : 'Black';

function gameStatus() {
  if(online?.room&&!online.state) return {title:'Connecting to room',detail:'Restoring your game from the server.'};
  if(online?.state&&!online.state.ready) return {title:'Waiting for your friend',detail:'You are White. Share the invite link to start.'};
  if (game.isCheckmate()) return {title:`${colorName(game.turn() === 'w' ? 'b' : 'w')} wins`,detail:'Checkmate. A well-played finish.'};
  if (game.isStalemate()) return {title:'Draw by stalemate',detail:'No legal moves, and the king is not in check.'};
  if (game.isThreefoldRepetition()) return {title:'Draw by repetition',detail:'The same position has occurred three times.'};
  if (game.isInsufficientMaterial()) return {title:'Draw',detail:'Neither side has enough material to checkmate.'};
  if (game.isDraw()) return {title:'Draw · 50-move rule',detail:'Fifty moves each without a pawn move or capture.'};
  return {title:`${colorName(game.turn())} to move${game.isCheck() ? ' · Check' : ''}`,detail:game.isCheck() ? 'Your king is in check. Move to safety, block, or capture.' : game.history().length ? 'Select a piece to see its legal moves.' : 'The board is yours. White moves first.'};
}

function renderBoard() {
  const board = $('board');
  const focused = document.activeElement?.dataset?.square;
  board.replaceChildren();
  const ranks = flipped ? [1,2,3,4,5,6,7,8] : [8,7,6,5,4,3,2,1];
  const files = flipped ? [...'hgfedcba'] : [...'abcdefgh'];
  const legal = selected ? game.moves({square:selected,verbose:true}) : [];
  const last = game.history({verbose:true}).at(-1);
  ranks.forEach((rank,row) => files.forEach((file,col) => {
    const square = file + rank, piece = game.get(square);
    const button = document.createElement('button');
    const target = legal.find(move => move.to === square);
    button.className = 'square' + ((file.charCodeAt(0)-97+rank)%2===1 ? ' dark' : '') + (selected===square ? ' selected' : '') + (last && [last.from,last.to].includes(square) ? ' last' : '') + (target ? ` legal${piece ? ' capture' : ''}` : '') + (piece?.type==='k' && piece.color===game.turn() && game.isCheck() ? ' check' : '');
    button.dataset.square = square;
    button.setAttribute('aria-label',`${square}${piece ? `, ${colorName(piece.color)} ${names[piece.type]}` : ', empty'}${target ? ', legal destination' : ''}`);
    button.setAttribute('aria-pressed',String(square===selected));
    button.tabIndex = square === (focused || selected || (flipped ? 'e8' : 'e2')) ? 0 : -1;
    if (piece) {
      const img = document.createElement('img'); img.src=`assets/${piece.color}${piece.type}.png`; img.alt=''; img.draggable=false;
      button.append(img);
    }
    if (col===0) {const label=document.createElement('span');label.className='coord rank';label.textContent=rank;button.append(label);}
    if (row===7) {const label=document.createElement('span');label.className='coord file';label.textContent=file;button.append(label);}
    button.onclick=()=>selectSquare(square);
    button.onkeydown=(event)=>{
      const directions={ArrowUp:-8,ArrowDown:8,ArrowLeft:-1,ArrowRight:1};
      if (event.key==='Escape') {selected=null;render();return;}
      if (!(event.key in directions)) return;
      event.preventDefault();
      const index=row*8+col, next=index+directions[event.key];
      if (next<0 || next>63 || (event.key==='ArrowLeft'&&col===0) || (event.key==='ArrowRight'&&col===7)) return;
      button.tabIndex=-1;board.children[next].tabIndex=0;board.children[next].focus();
    };
    board.append(button);
  }));
  if (focused) board.querySelector(`[data-square="${focused}"]`)?.focus({preventScroll:true});
}

function playerMarkup(color) {
  const captures=game.history({verbose:true}).filter(move=>move.color===color&&move.captured).map(move=>names[move.captured]);
  return `<div class="avatar"><img src="assets/${color}k.png" alt=""></div><div><div class="player-name">${colorName(color)}</div><div class="player-meta">${captures.length ? `${captures.length} ${captures.length===1?'piece':'pieces'} captured` : 'Ready at the board'}</div></div><span class="player-badge ${!game.isGameOver()&&game.turn()===color?'active':''}">${game.isGameOver()?'Finished':game.turn()===color?'Your turn':'Waiting'}</span>`;
}

function render() {
  renderBoard();
  $('top-player').innerHTML=playerMarkup(flipped?'w':'b');
  $('bottom-player').innerHTML=playerMarkup(flipped?'b':'w');
  const status=gameStatus(); $('status').textContent=status.title; $('status-detail').textContent=status.detail;
  $('turn-marker').classList.toggle('black',game.turn()==='b');
  const history=game.history(); $('move-count').textContent=`${history.length} played`; $('undo').disabled=!history.length||Boolean(online?.room);
  $('new-game').disabled=Boolean(online?.room);
  const container=$('history');
  if (!history.length) container.innerHTML='<div class="empty-history"><span>01</span><p>Every game starts<br>with a possibility.</p></div>';
  else {
    container.replaceChildren();
    for(let i=0;i<history.length;i+=2) {
      const row=document.createElement('div');row.className='move-row';
      [String(i/2+1),history[i],history[i+1]||'—'].forEach((text,index)=>{const span=document.createElement('span');span.textContent=text;if(index>0&&i+index-1===history.length-1)span.className='latest';row.append(span);});
      container.append(row);
    }
    container.scrollTop=container.scrollHeight;
  }
}

function playSound(capture) {
  if(!soundOn) return;
  try {
    audioContext ||= new (window.AudioContext||window.webkitAudioContext)();
    void audioContext.resume().catch(()=>{});
    const oscillator=audioContext.createOscillator(), gain=audioContext.createGain();
    oscillator.type='sine';oscillator.frequency.setValueAtTime(capture?240:440,audioContext.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(capture?100:220,audioContext.currentTime+.09);
    gain.gain.setValueAtTime(.12,audioContext.currentTime);gain.gain.exponentialRampToValueAtTime(.001,audioContext.currentTime+.12);
    oscillator.connect(gain);gain.connect(audioContext.destination);oscillator.start();oscillator.stop(audioContext.currentTime+.13);
  } catch { /* Audio is optional. */ }
}

async function makeMove(from,to,promotion='q') {
  if(moveBusy) throw new Error('A move is already being sent.');
  if(online?.room){
    if(online.state?.color!==game.turn()) throw new Error('It is the other player’s turn.');
    const legal=game.moves({square:from,verbose:true}).find(move=>move.to===to&&(!move.promotion||move.promotion===promotion));
    if(!legal)throw new Error('That move is not legal.');
    moveBusy=true;
    try {const data=await online.move(from+to+(legal.promotion||''));selected=null;render();playSound(Boolean(legal.captured));return {fen:data.fen,status:gameStatus().title};}
    finally{moveBusy=false;}
  }
  if(game.isGameOver()) throw new Error('The game has ended. Start a new game to play.');
  const move=game.move({from,to,promotion});
  selected=null;render();playSound(Boolean(move.captured));
  return {move:move.san,fen:game.fen(),status:gameStatus().title};
}

function selectSquare(square) {
  if(game.isGameOver()||pendingPromotion||moveBusy) return;
  if(online?.room&&(!online.connected||!online.state?.ready||online.state.color!==game.turn()))return;
  const moves=selected ? game.moves({square:selected,verbose:true}).filter(move=>move.to===square) : [];
  if(moves.length) {
    if(moves.some(move=>move.promotion)) {
      pendingPromotion={from:selected,to:square};
      $('promotion-options').replaceChildren();
      for(const type of ['q','r','b','n']) {
        const button=document.createElement('button');button.value=type;button.setAttribute('aria-label',`Promote to ${names[type]}`);
        const img=document.createElement('img');img.src=`assets/${game.turn()}${type}.png`;img.alt=names[type];button.append(img);$('promotion-options').append(button);
      }
      $('promotion').returnValue='cancel';$('promotion').showModal();return;
    }
    makeMove(selected,square).catch(showOnlineError);return;
  }
  selected=game.get(square)?.color===game.turn() && selected!==square ? square : null;
  render();
}

$('promotion').addEventListener('close',()=>{
  const pending=pendingPromotion;pendingPromotion=null;
  if(pending&&['q','r','b','n'].includes($('promotion').returnValue)) makeMove(pending.from,pending.to,$('promotion').returnValue).catch(showOnlineError);
});
$('undo').onclick=()=>{if(online?.room)return;game.undo();selected=null;render();};
$('flip').onclick=()=>{flipped=!flipped;render();};
$('sound').onclick=()=>{soundOn=!soundOn;$('sound').textContent=`Sound ${soundOn?'on':'off'}`;$('sound').setAttribute('aria-pressed',String(soundOn));playSound(false);};
$('new-game').onclick=()=>{if(game.history().length) {$('restart').returnValue='cancel';$('restart').showModal();}else{game.reset();selected=null;render();}};
$('restart').addEventListener('close',()=>{if($('restart').returnValue==='restart'){game.reset();selected=null;render();}});
document.querySelectorAll('[data-theme]').forEach(button=>button.onclick=()=>{document.body.dataset.theme=button.dataset.theme;document.querySelectorAll('.swatch').forEach(swatch=>swatch.setAttribute('aria-pressed',String(swatch===button)));});
document.addEventListener('keydown',event=>{if(event.key.toLowerCase()==='f'&&!event.ctrlKey&&!event.metaKey&&!event.altKey&&!document.querySelector('dialog[open]')){flipped=!flipped;render();}});
function showOnlineError(error){$('connection').textContent=error.message||String(error);}
let storage;
try{storage=window.localStorage;}catch{storage=null;}
online=new RoomClient({baseUrl:location.origin,storage,onState:(data)=>{
  if(seenVersion!==data.version){
    if(seenVersion===-1)flipped=data.color==='b';
    game.reset();for(const uci of data.moves)game.move({from:uci.slice(0,2),to:uci.slice(2,4),promotion:uci[4]||'q'});
    selected=null;seenVersion=data.version;
  }
  $('game-mode').textContent=`ONLINE · YOU ARE ${colorName(data.color).toUpperCase()}`;
  $('invite-box').hidden=false;$('leave-room').hidden=false;$('join-room').hidden=true;
  const invite=new URL(location.href);invite.search='';invite.searchParams.set('room',data.room);invite.hash='';
  $('invite-link').value=invite.href;history.replaceState(null,'',invite);
  document.querySelector('.small-note').textContent='Online rooms last seven days. Reopen this link in the same browser to resume.';
  render();
},onConnection:(message)=>{
  $('connection').textContent=message==='Connected'?`Connected as ${colorName(online.state.color)}. ${online.state.ready?'Moves update automatically.':'Waiting for your friend.'}`:message;
}});
async function roomAction(action){
  $('create-room').disabled=true;$('join-room').disabled=true;
  try{await action();}catch(error){showOnlineError(error);}finally{$('create-room').disabled=false;$('join-room').disabled=false;}
}
$('create-room').onclick=()=>roomAction(async()=>{seenVersion=-1;await online.create();});
const invitedRoom=new URL(location.href).searchParams.get('room');
$('join-room').onclick=()=>roomAction(async()=>{seenVersion=-1;await online.join(invitedRoom);});
$('copy-invite').onclick=async()=>{try{await navigator.clipboard.writeText($('invite-link').value);$('connection').textContent='Invite copied. Send it to your friend.';}catch{$('invite-link').select();$('connection').textContent='Select and copy the invite link above.';}};
$('leave-room').onclick=()=>{
  online.stop();seenVersion=-1;game.reset();selected=null;flipped=false;
  const url=new URL(location.href);url.search='';history.replaceState(null,'',url);
  $('invite-box').hidden=true;$('leave-room').hidden=true;$('join-room').hidden=true;
  $('game-mode').textContent='LOCAL CHESS';$('connection').textContent='Create a room and invite a friend on another device.';
  document.querySelector('.small-note').textContent='Pass the turn to a friend. No clocks. Take your time.';render();
};
if(invitedRoom){
  if(online.saved(invitedRoom))roomAction(()=>online.resume(invitedRoom));
  else{$('join-room').hidden=false;$('connection').textContent='You have been invited. Join to play as Black.';}
}
render();

// Optional agent access shares exactly the same state and move action as the board.
if (document.modelContext?.registerTool) {
  const lifecycle=new AbortController();
  window.addEventListener('pagehide',()=>lifecycle.abort(),{once:true});
  const register=(tool)=>{
    try { Promise.resolve(document.modelContext.registerTool(tool,{signal:lifecycle.signal})).catch(()=>{}); } catch { /* Unsupported experimental API. */ }
  };
  register({name:'read_chess_game',description:'Read the current position, legal moves, and game result.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true,untrustedContentHint:false},execute:()=>({fen:game.fen(),legalMoves:game.moves(),status:gameStatus().title})});
  register({name:'make_chess_move',description:'Play one legal move on the visible chessboard. Use algebraic square names and specify a piece for promotion.',inputSchema:{type:'object',properties:{from:{type:'string',pattern:'^[a-h][1-8]$'},to:{type:'string',pattern:'^[a-h][1-8]$'},promotion:{type:'string',enum:['q','r','b','n']}},required:['from','to'],additionalProperties:false},annotations:{readOnlyHint:false,untrustedContentHint:false},execute:(input)=>{
    if(!input||!Object.keys(input).every(key=>['from','to','promotion'].includes(key))||!(/^[a-h][1-8]$/).test(input.from)||!(/^[a-h][1-8]$/).test(input.to)||(input.promotion!==undefined&&!['q','r','b','n'].includes(input.promotion))) throw new Error('Provide valid from/to squares and an optional promotion piece.');
    if(document.querySelector('dialog[open]')) throw new Error('Close the active dialog before making a move.');
    return makeMove(input.from,input.to,input.promotion||'q');
  }});
}
