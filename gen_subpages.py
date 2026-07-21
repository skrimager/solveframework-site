import re

ROOT = '/home/user/workspace/brand_verify_site'

with open(f'{ROOT}/index.html') as f:
    index_content = f.read()

HEADER = re.search(r'(<header class="site-header".*?</header>)', index_content, re.DOTALL).group(1)
FOOTER = re.search(r'(<footer class="site-footer".*?</footer>)', index_content, re.DOTALL).group(1)

# Tracking script + script.js tag (shared boilerplate at the end of body)
TRACKING_SCRIPT = re.search(r'(<!-- Anonymous, privacy-respecting page-view tracking.*?</script>\n\n<script src="script.js"></script>)', index_content, re.DOTALL).group(1)

HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} | The SOLVE Framework&trade;</title>
<meta name="description" content="{description}" />
<meta property="og:title" content="{title} - The SOLVE Framework&trade;" />
<meta property="og:description" content="{description}" />
<meta property="og:type" content="website" />

<link rel="preconnect" href="https://api.fontshare.com" />
<link href="https://api.fontshare.com/v2/css?f[]=clash-grotesk@400,500,600,700&f[]=satoshi@400,500,600,700&display=swap" rel="stylesheet" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital@0;1&display=swap" rel="stylesheet" />

<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#050C1C">

<link rel="stylesheet" href="style.css" />
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

{header}

<main id="main">
{body}
</main>

{footer}

{tracking}
</body>
</html>
"""

def write_page(fname, title, description, body):
    html = HEAD_TEMPLATE.format(
        title=title,
        description=description,
        header=HEADER,
        body=body,
        footer=FOOTER,
        tracking=TRACKING_SCRIPT,
    )
    with open(f'{ROOT}/{fname}', 'w') as f:
        f.write(html)
    print(f'Wrote {fname}')


# ---------- Placeholder shells (user provides copy) ----------

placeholder_body = lambda eyebrow, title, note: f"""  <section class="subpage-hero">
    <div class="wrap">
      <span class="subpage-eyebrow">{eyebrow}</span>
      <h1 class="subpage-title">{title}</h1>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <div class="subpage-placeholder">
        <strong>Content pending</strong>
        {note}
      </div>
    </div>
  </section>
"""

write_page(
    'about-wade.html',
    'About Wade',
    "Wade Skrimager, creator of The SOLVE Framework.",
    placeholder_body(
        'About',
        'About Wade',
        'Wade is providing the full copy for this page directly. This is a structural shell only &mdash; no biography content has been drafted or auto-generated.',
    ),
)

write_page(
    'methodology.html',
    'Methodology & Real Call Scoring',
    "How The SOLVE Framework scores real conversations against a published rubric.",
    placeholder_body(
        'Product',
        'Methodology &amp; Real Call Scoring',
        'Wade is providing the full methodology copy directly. This is a structural shell only &mdash; no methodology content has been drafted or auto-generated.',
    ),
)

print('Done with placeholder shells.')
