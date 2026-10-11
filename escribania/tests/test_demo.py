import unittest
from fastapi.testclient import TestClient
import test_app as baseline
import app
from core import valid_ci
class DemoTests(unittest.TestCase):
 def test_public_demo_does_not_authenticate(self):
  with TestClient(app.app) as c:
   r=c.get('/demo');self.assertEqual(r.status_code,200);self.assertNotIn('escribania',r.cookies)
   self.assertIn('Solo ejemplo ficticio',r.text);self.assertIn('sin autenticador',r.text)
   self.assertEqual(c.get('/api/cases').status_code,401)
   self.assertEqual(c.post('/api/draft',json={}).status_code,403)
 def test_synthetic_identity_format(self):
  self.assertTrue(valid_ci('1.234.567-2'));self.assertTrue(valid_ci('2.345.678-3'))
 def test_demo_entry_and_supabase_signup_visible(self):
  with TestClient(app.app) as c:
   s=c.get('/').text;self.assertIn('href="/demo"',s);self.assertIn('Crear usuario con Supabase',s)
   self.assertIn('email-config-state',s)
