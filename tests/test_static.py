"""Static artifact integrity tests; not payment/backend security evidence."""
from pathlib import Path
from html.parser import HTMLParser
import base64
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.feed(text)
    def handle_starttag(self, tag, attributes):
        self.elements.append((tag, dict(attributes)))

class StaticPrototype(unittest.TestCase):
    def setUp(self):
        self.sources = [ROOT / 'public/index.html', ROOT / 'public/agenda/index.html']
        self.config = json.loads((ROOT / 'vercel.json').read_text())

    def test_two_complete_self_contained_documents(self):
        for source in self.sources:
            text = source.read_text()
            self.assertTrue(text.startswith('<!doctype html>'))
            self.assertTrue(text.rstrip().endswith('</body></html>'))
            self.assertNotIn('{{', text)
            document = Document(text)
            self.assertFalse(any(tag == 'script' and 'src' in attrs for tag, attrs in document.elements))
            self.assertFalse(any(tag == 'link' and attrs.get('rel') == 'stylesheet' for tag, attrs in document.elements))

    def test_unique_ids_and_label_targets(self):
        for source in self.sources:
            document = Document(source.read_text())
            ids = [attrs['id'] for _, attrs in document.elements if 'id' in attrs]
            self.assertEqual(len(ids), len(set(ids)))
            for tag, attrs in document.elements:
                if tag == 'label' and 'for' in attrs:
                    self.assertIn(attrs['for'], ids)

    def test_csp_hash_matches_each_inline_script(self):
        policy = next(x['value'] for x in self.config['headers'][0]['headers'] if x['key'] == 'Content-Security-Policy')
        for source in self.sources:
            scripts = re.findall(r'<script>([\s\S]*?)</script>', source.read_text())
            self.assertEqual(len(scripts), 1)
            digest = base64.b64encode(hashlib.sha256(scripts[0].encode()).digest()).decode()
            self.assertIn("'sha256-" + digest + "'", policy)
        self.assertIn("connect-src 'none'", policy)
        self.assertIn("form-action 'none'", policy)
        self.assertIn("frame-ancestors 'none'", policy)

    def test_no_external_communication_or_storage_in_code(self):
        script = (ROOT / 'src/prototype.js').read_text()
        for forbidden in ['fetch(', 'XMLHttpRequest', 'sendBeacon(', 'new WebSocket', 'localStorage', 'sessionStorage', 'document.cookie']:
            self.assertNotIn(forbidden, script)

    def test_explicit_simulation_markers(self):
        for source in self.sources:
            text = source.read_text()
            self.assertIn('Sem cobrança, reserva ou ingresso válido', text)
            self.assertIn('SEM VALIDADE PARA ENTRADA', text)
            self.assertIn('readonly aria-readonly="true"', text)
            self.assertIn('noindex,nofollow', text)

    def test_no_accidental_token_or_private_key(self):
        for source in [*self.sources, ROOT / 'src/prototype.js', ROOT / 'vercel.json']:
            text = source.read_text()
            self.assertIsNone(re.search(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----)', text))

    def test_static_deploy_settings(self):
        self.assertEqual(self.config['outputDirectory'], 'public')
        self.assertEqual(self.config['buildCommand'], '')
        self.assertIsNone(self.config['framework'])
        self.assertFalse((ROOT / 'package.json').exists())

if __name__ == '__main__':
    unittest.main()
