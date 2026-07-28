import re

ROOT = '/home/user/workspace/brand_verify_site'

with open(f'{ROOT}/index.html') as f:
    index_content = f.read()

HEADER = re.search(r'(<header class="site-header".*?</header>)', index_content, re.DOTALL).group(1)
FOOTER = re.search(r'(<footer class="site-footer".*?</footer>)', index_content, re.DOTALL).group(1)
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
    html = HEAD_TEMPLATE.format(title=title, description=description, header=HEADER, body=body, footer=FOOTER, tracking=TRACKING_SCRIPT)
    with open(f'{ROOT}/{fname}', 'w') as f:
        f.write(html)
    print(f'Wrote {fname}')

# FAQ content sourced strictly from facts already published on:
# - index.html #pricing section (seat tiers, dashboard, ROI, credits, referral)
# - terms-of-service.html (billing/cancellation, practice-hour limits, credit rules)
# - index.html #platform, #framework, #leadership sections (product facts)
faqs = [
    ("What is The SOLVE Framework?", "The SOLVE Framework is a five-step, consultative approach to discovery and leadership: Situation, Open with Questions, Listen for the Outcome, Visualize Success, and Engineer the Solution. The SOLVE Platform&trade; lets your team practice it in realistic, AI-powered conversations and get scored against that same published rubric."),
    ("How much does a consultant seat cost?", "Seats are billed monthly per seat, based on your total seat count: $49/seat for Team (1-5 seats), $45/seat for Office (6-20 seats), and $41/seat for Company (21-35 seats). Enterprise (36+ seats) is a custom quote. Each seat includes up to 10 hours of practice session time per calendar month."),
    ("Is there a free trial?", "Yes. Every team member gets one free practice session with no credit card required. A five-person team can run five real, scored practice conversations before spending a dollar. After that, billing is monthly and you can cancel anytime."),
    ("Do I need the Manager Dashboard to practice?", "No. The Manager Dashboard is an optional add-on at every tier and is not required to practice. A manager who wants to practice personally simply adds their own consultant seat at the normal per-seat rate."),
    ("Can I cancel anytime?", "Yes. Subscriptions renew automatically unless cancelled, and you can cancel at any time. Cancelling stops future billing, but it does not refund amounts already charged, except where required by law or separately stated at the time of purchase."),
    ("Is there a limit on how much I can practice?", "Each consultant seat includes up to 10 hours of practice session time per calendar month, which keeps per-seat pricing low. If a seat reaches its monthly limit, additional practice sessions may be paused for the rest of that calendar month."),
    ("Can I upload real calls or transcripts to get scored?", "Yes. You can upload real call recordings, transcripts, or text/email exchanges and get them scored by SOLVE Coach&trade; against the same five-step rubric your team certifies on. This is limited to 20 submissions per consultant seat per calendar month, and you're responsible for having the right to any recording you submit, including consent where required by law."),
    ("What is the certification path?", "The SOLVE Academy certification track runs Beginner &rarr; Intermediate &rarr; Advanced &rarr; Certified. Each level requires a score of 85% or better to advance. Passing the Expert-level exam earns official SOLVE Framework Certification, a certificate, and a challenge coin."),
    ("Does SOLVE cover conflict management, or only sales discovery?", "Both. Every seat includes two tracks: Consultation &amp; Discovery and Conflict Resolution (SOLVE Leadership&trade;). Conflict Resolution applies the same five-step method to upset customer service, employee grievances, and peer-to-peer team conflict, with its own certification path."),
    ("Do I get credit back as my team improves?", "Yes. Certification milestones (SOLVE Certified Consultant, Conflict Management Certified, Cross-Industry Certified, and Master SOLVE Academy Consultant) each earn a $50 account credit, up to $200 per consultant. Credits apply automatically to future invoices, can cover up to 50% of a single invoice, and are earned only by consultants on seats active for at least 60 days. Credits carry no cash value, are non-transferable and non-refundable, and expire 12 months after issuance."),
    ("Is there a referral program?", "Yes. If a colleague sets up their own team and dashboard because of you, mention your company in the Request Access form. Once their account reaches its 60th active day, you receive a $100 credit automatically. There's no limit on how many times this can happen."),
    ("What if my industry isn't covered yet?", "If your business isn't already in the conversation library, SOLVE will build five custom scenarios for your specific industry at no additional cost, included with any account running the Manager Dashboard."),
]

items_html = "\n".join(
    f"""        <details class="faq-item reveal">
          <summary class="faq-question">{q}</summary>
          <div class="faq-answer"><p>{a}</p></div>
        </details>"""
    for q, a in faqs
)

body = f"""  <section class="subpage-hero">
    <div class="wrap">
      <span class="subpage-eyebrow">FAQ</span>
      <h1 class="subpage-title">Frequently Asked Questions</h1>
      <p class="section-sub center">Answers pulled directly from our published pricing, terms of service, and platform pages. If you don't see your question here, reach out and we'll add it.</p>
    </div>
  </section>
  <section class="section">
    <div class="wrap" style="max-width:var(--content-narrow);">
      <div class="faq-list">
{items_html}
      </div>
    </div>
  </section>
  <section class="section">
    <div class="wrap center">
      <div class="book-actions" style="justify-content:center;">
        <a href="https://training.solveframework.com" class="btn btn-primary btn-lg" data-testid="link-faq-demo-cta">Try the Demo</a>
        <a href="pricing.html" class="btn btn-outline-invert btn-lg" data-testid="link-faq-pricing-cta">See Pricing</a>
      </div>
    </div>
  </section>
"""

write_page(
    'faq.html',
    'FAQ',
    'Frequently asked questions about SOLVE Platform pricing, free trial, cancellation, certification, and conflict resolution training.',
    body,
)
