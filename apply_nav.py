import re

NAV_SNIPPET = open('/home/user/workspace/brand_verify_site/nav_snippet.html').read().rstrip('\n')

files = ['index.html', 'privacy-policy.html', 'terms-of-service.html', 'trademark-guidelines.html']

# Pattern matches the old <nav class="main-nav" ...> ... </nav> block (non-greedy, single nav in header)
pattern = re.compile(r'    <nav class="main-nav"[^>]*>.*?</nav>', re.DOTALL)

for fname in files:
    path = f'/home/user/workspace/brand_verify_site/{fname}'
    content = open(path).read()
    new_content, count = pattern.subn(NAV_SNIPPET, content, count=1)
    if count != 1:
        print(f'WARNING: {fname} - replaced {count} occurrences (expected 1)')
        continue
    open(path, 'w').write(new_content)
    print(f'{fname}: nav replaced OK')
