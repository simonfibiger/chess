import concurrent.futures
import tempfile
import unittest
from pathlib import Path
from server import create_app

class RoomsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'test.sqlite3'
        self.app = create_app(self.path)
        self.white = self.app.test_client()
        self.black = self.app.test_client()
        self.created = self.white.post('/api/rooms', json={}).get_json()
        self.url = '/api/rooms/' + self.created['room']
        self.wh = {'Authorization': 'Bearer ' + self.created['token']}
    def tearDown(self):
        self.temp.cleanup()
    def join(self):
        joined = self.black.post(self.url + '/join', json={})
        self.assertEqual(joined.status_code, 200)
        self.bh = {'Authorization': 'Bearer ' + joined.json['token']}
        return joined.json
    def move(self, client, headers, uci, version=None):
        if version is None:
            version = client.get(self.url, headers=headers).json['version']
        return client.post(self.url+'/moves', json={'move':uci,'version':version},headers=headers)
    def test_two_clients_and_reconnect(self):
        self.assertEqual(self.move(self.white,self.wh,'e2e4').status_code,409)
        self.join()
        self.assertEqual(self.move(self.black,self.bh,'e7e5').status_code,403)
        self.assertEqual(self.move(self.white,self.wh,'e2e5').status_code,400)
        self.assertEqual(self.move(self.white,self.wh,'e2e2').status_code,400)
        self.assertEqual(self.move(self.white,self.wh,'e2e4').status_code,200)
        self.assertEqual(self.move(self.black,self.bh,'e7e5').status_code,200)
        a=self.white.get(self.url,headers=self.wh).json
        b=self.black.get(self.url,headers=self.bh).json
        self.assertEqual(a['fen'],b['fen'])
        self.assertEqual(a['moves'],['e2e4','e7e5'])
        restarted=create_app(self.path).test_client().get(self.url,headers=self.wh)
        self.assertEqual(restarted.json['fen'],a['fen'])
        self.assertEqual(restarted.json['color'],'w')
    def test_authentication_and_full_room(self):
        self.join()
        self.assertEqual(self.app.test_client().post(self.url+'/join',json={}).status_code,409)
        self.assertEqual(self.white.get(self.url).status_code,401)
        self.assertEqual(self.white.get(self.url,headers={'Authorization':'Bearer fake'}).status_code,403)
        self.assertNotIn('token',self.white.get(self.url,headers=self.wh).json)
        self.assertEqual(self.white.post('/api/rooms',json={},headers={'Origin':'https://wrong.example'}).status_code,403)
        self.assertEqual(self.white.post('/api/rooms',json=[]).status_code,400)
    def test_concurrent_moves_only_one_wins(self):
        joined=self.join()
        def attempt(uci):
            return self.move(self.app.test_client(),self.wh,uci,joined['version']).status_code
        with concurrent.futures.ThreadPoolExecutor(2) as pool:
            results=list(pool.map(attempt,['e2e4','d2d4']))
        self.assertEqual(sorted(results),[200,409])
        self.assertEqual(len(self.white.get(self.url,headers=self.wh).json['moves']),1)
    def test_concurrent_join_only_one_wins(self):
        with concurrent.futures.ThreadPoolExecutor(2) as pool:
            results=list(pool.map(lambda _:self.app.test_client().post(self.url+'/join',json={}).status_code,range(2)))
        self.assertEqual(sorted(results),[200,409])
    def test_checkmate_stops_game(self):
        self.join()
        for client,headers,uci in [(self.white,self.wh,'f2f3'),(self.black,self.bh,'e7e5'),(self.white,self.wh,'g2g4'),(self.black,self.bh,'d8h4')]:
            response=self.move(client,headers,uci)
            self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['result'],'0-1')
        self.assertEqual(response.json['reason'],'checkmate')
        self.assertEqual(self.move(self.white,self.wh,'a2a3').status_code,409)
    def test_special_moves(self):
        self.join()
        for i,uci in enumerate(['e2e4','a7a6','e4e5','d7d5','e5d6']):
            response=self.move(self.white if i%2==0 else self.black,self.wh if i%2==0 else self.bh,uci)
            self.assertEqual(response.status_code,200)
        self.assertTrue(response.json['fen'].startswith('rnbqkbnr/1pp1pppp/p2P4'))
    def test_static_server_does_not_expose_database(self):
        with self.white.get('/') as response:
            self.assertEqual(response.status_code,200)
        self.assertEqual(self.white.get('/server.py').status_code,404)
        self.assertEqual(self.white.get('/data/rooms.sqlite3').status_code,404)

if __name__=='__main__':
    unittest.main()
