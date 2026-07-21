import re

files_login_label = {
    'index.html': 'Get Started',
    'privacy-policy.html': 'Log In',
    'terms-of-service.html': 'Log In',
    'trademark-guidelines.html': 'Log In',
}

NEW_LINKS_TEMPLATE = """      <a href="methodology.html">Methodology</a>
      <a href="certification.html">Certification</a>
      <a href="manager-dashboard.html">Manager Dashboard</a>
      <a href="why-solve-works.html">Why SOLVE Works</a>
      <a href="research.html">Research</a>
      <a href="conflict-resolution.html">Conflict Resolution</a>
      <a href="about-wade.html">About Wade</a>
      <a href="books.html">Books</a>
      <a href="pricing.html">Pricing</a>
      <a href="faq.html">FAQ</a>
      <a href="https://training.solveframework.com">{login_label}</a>
      <a href="https://training.solveframework.com/admin/login">Vault</a>
      <a href="privacy-policy.html">Privacy Policy</a>
      <a href="terms-of-service.html">Terms of Service</a>
      <a href="trademark-guidelines.html">Trademark Guidelines</a>"""

pattern = re.compile(r'    <nav class="footer-nav"[^>]*>\n(.*?)\n    </nav>', re.DOTALL)

for fname, login_label in files_login_label.items():
    path = f'/home/user/workspace/brand_verify_site/{fname}'
    content = open(path).read()
    new_links = NEW_LINKS_TEMPLATE.format(login_label=login_label)
    def repl(m):
        return '    <nav class="footer-nav" aria-label="Footer">\n' + new_links + '\n    </nav>'
    new_content, count = pattern.subn(repl, content, count=1)
    if count != 1:
        print(f'WARNING: {fname} - replaced {count} (expected 1)')
        continue
    open(path, 'w').write(new_content)
    print(f'{fname}: footer nav replaced OK')
