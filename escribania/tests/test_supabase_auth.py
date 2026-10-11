import base64,json,time,unittest
from unittest.mock import patch,AsyncMock
from fastapi.testclient import TestClient
import test_app as baseline
import app
import supabase_auth as auth

UID='11111111-1111-4111-8111-111111111111'
ENV={'SUPABASE_URL':'https://testproject.supabase.co','SUPABASE_PUBLISHABLE_KEY':'sb_publishable_FICTICIO','ESCRIBANIA_ALLOWED_EMAILS':'persona@example.test'}
def token(aal='aal2',sub=UID):
 payload=base64.urlsafe_b64encode(json.dumps({'aal':aal,'sub':sub}).encode()).decode().rstrip('=')
 return 'header.'+payload+'.signature'
def account(factors=None):return {'id':UID,'email':'persona@example.test','email_confirmed_at':'2026-10-11T12:00:00Z','factors':factors or []}

class SupabaseTests(unittest.IsolatedAsyncioTestCase):
 def setUp(self):self.env=patch.dict('os.environ',ENV);self.env.start()
 def tearDown(self):self.env.stop()
 async def test_unapproved_email_no_request(self):
  with patch.object(auth,'call',new_callable=AsyncMock) as call:
   with self.assertRaises(auth.AuthError):await auth.begin('otra@example.test','FicticiaPassword123')
   call.assert_not_awaited()
 async def test_begin_enrolls_without_app_session(self):
  with patch.object(auth,'call',new_callable=AsyncMock,side_effect=[{'access_token':'private'},account(),{'id':'factor','totp':{'secret':'PRIVATE-FICTITIOUS'}}]) as call:
   result=await auth.begin('persona@example.test','FicticiaPassword123')
   self.assertEqual(result['secret'],'PRIVATE-FICTITIOUS');self.assertEqual(result['uid'],UID)
   self.assertEqual(call.await_args_list[-1].args[1],'factors')
 async def test_existing_factor_does_not_reenroll(self):
  with patch.object(auth,'call',new_callable=AsyncMock,side_effect=[{'access_token':'private'},account([{'id':'factor','factor_type':'totp','status':'verified'}])]) as call:
   result=await auth.begin('persona@example.test','FicticiaPassword123');self.assertIsNone(result['secret']);self.assertEqual(call.await_count,2)
 async def test_unconfirmed_email_blocked(self):
  u=account();u['email_confirmed_at']=None
  with patch.object(auth,'call',new_callable=AsyncMock,side_effect=[{'access_token':'private'},u]):
   with self.assertRaises(auth.AuthError):await auth.begin('persona@example.test','FicticiaPassword123')
 async def test_mfa_remote_validation_and_aal2(self):
  with patch.object(auth,'call',new_callable=AsyncMock,side_effect=[{'id':'challenge'},{'access_token':token()},account()]) as call:
   self.assertEqual(await auth.finish({'token':'private','factor':'factor','uid':UID},'123456'),'supabase:'+UID)
   self.assertEqual(call.await_args_list[-1].args[1],'user')
 async def test_aal1_and_wrong_identity_rejected(self):
  for bad in [token('aal1'),token(sub='22222222-2222-4222-8222-222222222222')]:
   with patch.object(auth,'call',new_callable=AsyncMock,side_effect=[{'id':'challenge'},{'access_token':bad},account()]):
    with self.assertRaises(auth.AuthError):await auth.finish({'token':'private','factor':'factor','uid':UID},'123456')
 async def test_server_config_fails_closed(self):
  with patch.dict('os.environ',{'SUPABASE_URL':'https://example.test','ESCRIBANIA_ALLOWED_EMAILS':''}):
   self.assertFalse(auth.readiness()['enabled'])
   with self.assertRaises(auth.AuthError):auth.config()

class SupabaseRoutes(unittest.TestCase):
 def setUp(self):
  app.failures.clear();app.pending_auth.clear();self.client=TestClient(app.app);self.origin={'Origin':app.ORIGIN}
 def test_begin_is_preauth_only_and_finish_requires_csrf(self):
  pending={'token':'SUPABASE_PRIVATE_FICTITIOUS','factor':'factor','uid':UID,'secret':'TOTP_FICTITIOUS'}
  with patch.object(auth,'begin',new_callable=AsyncMock,return_value=pending):
   r=self.client.post('/api/auth/begin',headers=self.origin,json={'email':'persona@example.test','password':'FicticiaPassword123'})
  self.assertEqual(r.status_code,200);self.assertNotIn('SUPABASE_PRIVATE',r.text)
  self.assertEqual(self.client.get('/api/cases').status_code,401)
  self.assertEqual(self.client.post('/api/auth/finish',headers=self.origin,json={'otp':'123456'}).status_code,403)
  headers={**self.origin,'X-CSRF-Token':r.json()['csrf']}
  with patch.object(auth,'finish',new_callable=AsyncMock,return_value='supabase:'+UID):
   done=self.client.post('/api/auth/finish',headers=headers,json={'otp':'123456'})
  self.assertEqual(done.status_code,200);self.assertEqual(self.client.get('/api/me').json()['user'],'supabase:'+UID)
  self.assertEqual(self.client.post('/api/auth/finish',headers=headers,json={'otp':'123456'}).status_code,403)
 def test_wrong_origin_denied(self):
  for path in ('signup','begin','finish'):
   self.assertEqual(self.client.post('/api/auth/'+path,headers={'Origin':'https://foreign.example'},json={}).status_code,403)
 def test_expired_challenge_denied(self):
  app.pending_auth['expired']={'csrf':'test','expires':time.time()-1}
  self.client.cookies.set('escribania_setup','expired')
  self.assertEqual(self.client.post('/api/auth/finish',headers={**self.origin,'X-CSRF-Token':'test'},json={}).status_code,403)
 def test_signup_never_returns_tokens(self):
  with patch.object(auth,'signup',new_callable=AsyncMock,return_value={'access_token':'PRIVATE','user':account()}):
   r=self.client.post('/api/auth/signup',headers=self.origin,json={'email':'persona@example.test','password':'FicticiaPassword123'})
  self.assertEqual(r.status_code,200);self.assertNotIn('PRIVATE',r.text);self.assertEqual(self.client.get('/api/me').status_code,401)
