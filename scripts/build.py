#!/usr/bin/env python3
"""Compile two dependency-free, self-contained static prototypes."""
from pathlib import Path
import base64
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
css = (ROOT / 'src/prototype.css').read_text()
js = (ROOT / 'src/prototype.js').read_text()
template = (ROOT / 'src/template.html').read_text()
variants = [
    ('index.html', {
        'VARIANT_NAME': 'Descoberta editorial', 'BODY_CLASS': 'editorial',
        'HOME_LINK': './', 'OTHER_LINK': 'agenda/', 'OTHER_LABEL': 'Comparar: agenda',
        'EYEBROW': 'A cidade tem um encontro com você',
        'HEADING': 'Encontre o som<br>da sua próxima noite.',
        'INTRO': 'Explore os shows, escolha seu lugar e confira o valor completo antes de continuar.',
        'LIST_HEADING': 'Acontece por aqui',
    }),
    ('agenda/index.html', {
        'VARIANT_NAME': 'Agenda direta', 'BODY_CLASS': 'agenda',
        'HOME_LINK': '../', 'OTHER_LINK': '../', 'OTHER_LABEL': 'Comparar: descoberta',
        'EYEBROW': 'Sua agenda, no seu ritmo',
        'HEADING': 'Escolha a data.<br>Encontre o encontro.',
        'INTRO': 'Uma alternativa mais objetiva: filtros ao lado, datas em destaque e o caminho da compra sem distrações.',
        'LIST_HEADING': 'Na agenda',
    }),
]
for filename, values in variants:
    result = template
    for key, value in {'CSS': css, 'JS': js, **values}.items():
        result = result.replace('{{' + key + '}}', value)
    if '{{' in result:
        raise ValueError('Unresolved template placeholder')
    target = ROOT / 'public' / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(result)
    print(f'Built public/{filename}: {len(result.encode())} bytes')
script_hash = base64.b64encode(hashlib.sha256(js.encode()).digest()).decode()
policy = "default-src 'none'; script-src 'sha256-" + script_hash + "'; style-src 'unsafe-inline'; img-src 'self' data:; connect-src 'none'; font-src 'self'; base-uri 'none'; object-src 'none'; form-action 'none'; frame-ancestors 'none'"
configuration = {
    '$schema': 'https://openapi.vercel.sh/vercel.json',
    'framework': None, 'buildCommand': '', 'outputDirectory': 'public',
    'headers': [{'source': '/(.*)', 'headers': [
        {'key': 'Content-Security-Policy', 'value': policy},
        {'key': 'X-Content-Type-Options', 'value': 'nosniff'},
        {'key': 'X-Frame-Options', 'value': 'DENY'},
        {'key': 'Referrer-Policy', 'value': 'strict-origin-when-cross-origin'},
        {'key': 'Permissions-Policy', 'value': 'camera=(), microphone=(), geolocation=(), payment=()'},
    ]}],
}
(ROOT / 'vercel.json').write_text(json.dumps(configuration, ensure_ascii=False, indent=2) + '\n')
