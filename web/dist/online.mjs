export class RoomClient {
  constructor({baseUrl, storage, onState=()=>{}, onConnection=()=>{}}) {
    this.baseUrl=baseUrl;this.storage=storage;this.onState=onState;this.onConnection=onConnection;
    this.room=null;this.token=null;this.state=null;this.connected=false;this.generation=0;this.timer=null;
  }
  async request(path, {method='GET',body,token=this.token}={}) {
    let response;
    try {response=await fetch(new URL(path,this.baseUrl),{method,headers:{...(body?{'Content-Type':'application/json'}:{}),...(token?{Authorization:`Bearer ${token}`}:{})},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(10000)});}
    catch {throw new Error('Cannot reach the game server. Keep it running; reconnecting automatically.');}
    let data;
    try {data=await response.json();} catch {throw new Error('Online play needs the Python server. Open the game from its address.');}
    if(!response.ok) throw new Error(data.error||'The server could not complete that action.');
    return data;
  }
  saved(room) {try{return this.storage?.getItem(`chess-room:${room}`)||null;}catch{return null;}}
  apply(data) {
    if(this.state?.room===data.room&&this.state.version>data.version)return;
    this.state=data;this.connected=true;this.onState(data);this.onConnection('Connected');
  }
  adopt(data) {
    this.stop();this.room=data.room;this.token=data.token;
    try {this.storage?.setItem(`chess-room:${this.room}`,this.token);}catch{/* Session still works without storage. */}
    this.apply(data);this.schedule();return data;
  }
  async create() {return this.adopt(await this.request('/api/rooms',{method:'POST',body:{},token:null}));}
  async join(room) {return this.adopt(await this.request(`/api/rooms/${encodeURIComponent(room)}/join`,{method:'POST',body:{},token:null}));}
  async resume(room) {
    const token=this.saved(room);if(!token)return false;
    this.stop();this.room=room;this.token=token;
    try {await this.sync();} finally {this.schedule();}
    return true;
  }
  async sync() {
    const generation=this.generation,room=this.room;
    if(!room)return;
    try {const data=await this.request(`/api/rooms/${encodeURIComponent(room)}`);if(generation===this.generation)this.apply(data);}
    catch(error){if(generation===this.generation){this.connected=false;this.onConnection(error.message);}throw error;}
  }
  schedule() {
    clearTimeout(this.timer);
    this.timer=setTimeout(async()=>{try{await this.sync();}catch{}finally{if(this.room)this.schedule();}},1000);
  }
  async move(move) {
    if(!this.room||!this.connected||!this.state?.ready)throw new Error('Wait until both players are connected to the room.');
    const generation=this.generation;
    try {
      const data=await this.request(`/api/rooms/${this.room}/moves`,{method:'POST',body:{move,version:this.state.version}});
      if(generation===this.generation)this.apply(data);
      return data;
    } catch(error){try{await this.sync();}catch{}throw error;}
  }
  stop() {this.generation++;clearTimeout(this.timer);this.room=null;this.token=null;this.state=null;this.connected=false;}
}
