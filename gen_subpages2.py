import re

ROOT = '/home/user/workspace/brand_verify_site'
SEC = f'{ROOT}/_sections'

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

def read_section(name):
    with open(f'{SEC}/{name}.html') as f:
        return f.read()

def hero(eyebrow, title, sub=''):
    sub_html = f'<p class="section-sub center">{sub}</p>' if sub else ''
    return f"""  <section class="subpage-hero">
    <div class="wrap">
      <span class="subpage-eyebrow">{eyebrow}</span>
      <h1 class="subpage-title">{title}</h1>
      {sub_html}
    </div>
  </section>
"""

def cta_band():
    return """  <section class="section">
    <div class="wrap center">
      <div class="book-actions" style="justify-content:center;">
        <a href="https://training.solveframework.com" class="btn btn-primary btn-lg" data-testid="link-subpage-demo-cta">Try the Demo</a>
        <a href="pricing.html" class="btn btn-outline-invert btn-lg" data-testid="link-subpage-pricing-cta">See Pricing</a>
      </div>
    </div>
  </section>
"""

# ---------- Why SOLVE Works ----------
why_body = (
    hero('Why SOLVE', 'Why SOLVE Works', 'The thinking behind the method, why it is engineered rather than random, and how it stacks up against generic AI chat and traditional role-play.')
    + read_section('why')
    + read_section('framework')
    + read_section('why-different')
    + read_section('engineered')
    + read_section('objections')
    + read_section('real-conversations')
    + read_section('compare')
    + cta_band()
)
write_page(
    'why-solve-works.html',
    'Why SOLVE Works',
    'Why The SOLVE Framework is engineered, not random: the method, the rubric, real call scoring, and how it compares to generic AI chat and traditional role-play.',
    why_body,
)

# ---------- Research ----------
research_body = (
    hero('Why SOLVE', 'Research', 'SOLVE is built on published, peer-reviewed research about discovery, objection handling, and decision-making, not guesswork.')
    + """  <section class="section">
    <div class="wrap">
      <div class="research-strip reveal">
        <p class="research-strip-title">This isn't theory. It's documented.</p>
        <p class="research-strip-item">Research analyzing 35,000+ sales calls found top performers received fewer objections, because of superior discovery, not better comebacks. Many objections are created by the seller pitching before understanding. (Neil Rackham, SPIN Selling, Huthwaite research)</p>
        <p class="research-strip-item">Telling someone they're free to say no roughly doubles compliance rates, confirmed across 40+ studies with more than 22,000 participants. Affirming autonomy beats applying pressure. (Carpenter, "But You Are Free" meta-analysis, 2013)</p>
        <p class="research-strip-item">Customers who vividly imagine using a solution show significantly higher purchase intent. If they can't picture "solved," they haven't decided. (Gregory, Cialdini &amp; Carpenter, 1982; supported by decades of customer-orientation research, Franke &amp; Park, 2006)</p>
      </div>
      <p class="hook-closer">Script-based selling overcomes objections. SOLVE-based selling makes most of them never come up, and diagnoses the ones that do.</p>
    </div>
  </section>
"""
    + cta_band()
)
write_page(
    'research.html',
    'Research',
    'The published research behind The SOLVE Framework: discovery, objection handling, and decision science.',
    research_body,
)

# ---------- Certification ----------
cert_platform_raw = read_section('platform')
# Keep only the cert-levels block + intro copy; drop manager-pitch + book-actions (those go elsewhere)
cert_body = (
    hero('Product', 'Certification', 'Three levels of difficulty, one published rubric, and an official credential when you pass.')
    + """  <section class="section platform-section">
    <div class="wrap platform-inner">
      <div class="platform-copy reveal">
        <p class="eyebrow">The Best Discovery Practice on the Market</p>
        <h2 class="section-title">Practice the Framework. Get Certified.</h2>
        <p class="section-sub">The SOLVE Platform&trade; puts you inside realistic, AI-powered discovery conversations across dozens of real-world conversations, with instant, rubric-based feedback from SOLVE Coach&trade; so every rep gets sharper every time. Work through the SOLVE Academy&trade; certification track across three levels of difficulty and you earn SOLVE Framework Certification.</p>
        <div class="cert-levels">
          <a href="https://training.solveframework.com" class="cert-level" data-testid="link-cert-beginner">
            <img class="cert-badge" src="assets/badges/badge_beginner_v2.png" alt="SOLVE Academy Beginner Level Badge" loading="lazy" width="110" height="144">
            <h3>Beginner</h3>
            <p>Learn the five steps and run guided discovery conversations. Score 85% or better to advance.</p>
          </a>
          <a href="https://training.solveframework.com" class="cert-level" data-testid="link-cert-intermediate">
            <img class="cert-badge" src="assets/badges/badge_intermediate_v2.png" alt="SOLVE Academy Intermediate Level Badge" loading="lazy" width="110" height="144">
            <h3>Intermediate</h3>
            <p>Handle real objections and harder personas while keeping the customer's goal in focus. Score 85% or better to advance.</p>
          </a>
          <a href="https://training.solveframework.com" class="cert-level" data-testid="link-cert-advanced">
            <img class="cert-badge" src="assets/badges/badge_advanced_v2.png" alt="SOLVE Academy Advanced Level Badge" loading="lazy" width="110" height="144">
            <h3>Advanced</h3>
            <p>Run full discovery-to-close conversations under pressure. Score 85% or better to unlock the certification exam.</p>
          </a>
          <a href="https://training.solveframework.com" class="cert-level cert-level-final" data-testid="link-cert-certified">
            <div class="cert-final-copy">
              <span class="cert-final-eyebrow">What you take home</span>
              <h3>Certified</h3>
              <p>Pass the Expert-level exam and become <strong>SOLVE Framework Certified</strong>, proof you can turn any customer's needs and wants into a solved outcome. Issued through the SOLVE Academy certification track.</p>
            </div>
            <div class="cert-rewards">
              <figure class="cert-reward">
                <img src="assets/badges/coins_v2.png" alt="SOLVE Framework certification coins in bronze, silver and gold tiers" loading="lazy" width="900" height="401">
                <figcaption>Certification coin</figcaption>
              </figure>
              <figure class="cert-reward">
                <img src="assets/badges/certificate_v2.png" alt="Printed SOLVE Framework Certified Consultant certificate" loading="lazy" width="800" height="622">
                <figcaption>Printed certificate</figcaption>
              </figure>
              <figure class="cert-reward">
                <img src="assets/badges/award_v2.png" alt="Crystal SOLVE Framework Certified desk award" loading="lazy" width="700" height="586">
                <figcaption>Crystal desk award</figcaption>
              </figure>
            </div>
          </a>
        </div>
        <div class="book-actions">
          <a href="https://training.solveframework.com" class="btn btn-primary btn-lg" data-testid="link-platform-cta">Start Practicing</a>
        </div>
      </div>
    </div>
  </section>
"""
    + read_section('custom-industries')
    + cta_band()
)
write_page(
    'certification.html',
    'Certification',
    'The SOLVE Academy certification path: Beginner, Intermediate, Advanced, and Certified, scored against one published rubric.',
    cert_body,
)

# ---------- Manager Dashboard ----------
dashboard_body = (
    hero('Product', 'Manager Dashboard', 'Know who is practicing, who is improving, and who is ready for a real customer, at a glance for your whole team.')
    + """  <section class="section platform-section">
    <div class="wrap platform-inner">
      <div class="platform-copy reveal">
        <div class="manager-pitch reveal">
          <p class="eyebrow">For Team Managers</p>
          <h3>Certified reps don't have to ask for referrals. Clients just give them.</h3>
          <p>Every manager reminds their team to ask for referrals, because most reps never earned the right to skip the ask. SOLVE Framework Certification is proof your consultant can qualify and solve nearly every customer's real need, not just close the deal in front of them. When someone genuinely feels solved for, they don't wait to be asked. They refer people on their own.</p>
          <p>Get your whole team certified and you're not managing a group of closers anymore - you're running a team clients actively recommend.</p>
        </div>
        <ul class="platform-points">
          <li>Your reps build real conversational instincts in live discovery conversations with an AI customer</li>
          <li>Every session comes back scored by SOLVE Coach against the same five-step SOLVE rubric from the books, so reps know exactly what to fix</li>
          <li>Onboard consistently whether you're a single team or 1,000+ professionals</li>
          <li>Know who's ready before you turn them loose on customers, with the SOLVE Platform manager dashboard</li>
        </ul>
        <div class="book-actions">
          <a href="https://training.solveframework.com/#/dashboard-demo" class="btn btn-primary btn-lg" data-testid="link-managers-dashboard-demo">Explore the Demo Dashboard <span aria-hidden="true">&rarr;</span></a>
        </div>
      </div>
    </div>
  </section>
  <section class="section screenshots-section">
    <div class="wrap">
      <p class="eyebrow center">See It In Action</p>
      <h2 class="section-title center">A look inside the Manager Dashboard</h2>
      <p class="section-sub center">This is exactly what a manager sees once they log in.</p>
      <div class="screenshot-grid">
        <figure class="screenshot-card reveal">
          <img src="assets/screenshots/manager-roster.png" alt="Screenshot of the SOLVE Platform manager dashboard showing an office invite code, summary tiles for sessions completed, average discovery score, and in progress, and a consultant roster table listing each rep's tier, certification, progress, conversations, average score, and last active date, with Sofia Castellano Certified at the top" loading="lazy" />
          <figcaption>Your manager dashboard: every rep's tier, certification progress, and score at a glance. Know who's ready, who's improving, and who needs coaching.</figcaption>
        </figure>
        <figure class="screenshot-card reveal">
          <img src="assets/screenshots/manager-drilldown.png" alt="Screenshot of an individual rep drill-down on the SOLVE Platform manager dashboard showing Sofia Castellano's full conversation history with conversation name, track, score, status, and date for each session" loading="lazy" />
          <figcaption>Click any rep to see every conversation, every score, and their progress over time.</figcaption>
        </figure>
        <figure class="screenshot-card reveal">
          <img src="assets/screenshots/manager-command-center.png" alt="Screenshot of the SOLVE Academy Command Center dashboard showing team performance score, practice sessions, average score, certifications earned, a team performance overview chart, SOLVE Framework mastery radar, top performers, scenario breakdown, and level distribution" loading="lazy" />
          <figcaption>Build your data command center as your team levels up and grows.</figcaption>
        </figure>
      </div>
    </div>
  </section>
"""
    + cta_band()
)
write_page(
    'manager-dashboard.html',
    'Manager Dashboard',
    'The SOLVE Platform manager dashboard: certification progress, live scoring analytics, and per-rep drill-downs for your whole team.',
    dashboard_body,
)

# ---------- Conflict Resolution ----------
conflict_body = (
    hero('Conflict Resolution', 'SOLVE Leadership: Conflict Management &amp; Resolution', 'The same five-step method, applied to the conversations no one wants to have.')
    + read_section('leadership')
    + cta_band()
)
write_page(
    'conflict-resolution.html',
    'Conflict Resolution',
    'SOLVE Leadership: practice upset customer service, employee grievances, and peer-to-peer conflict with the same method and scoring as SOLVE discovery training.',
    conflict_body,
)

# ---------- Books ----------
books_body = (
    hero('About', 'Books', 'The companion reading behind The SOLVE Framework, for the individual conversation, the company around it, and the conflicts that test it.')
    + read_section('books')
    + read_section('membership')
)
write_page(
    'books.html',
    'Books',
    "Stop Selling. Start Solving., Uncommon CENTS, and Stay Calm and Resolve, the books behind The SOLVE Framework, by Wade Skrimager.",
    books_body,
)

# ---------- Pricing (empty placeholder shell per Step 4, per user instruction) ----------
pricing_body = (
    hero('Pricing', 'Pricing', 'Full seat and Manager Dashboard pricing detail.')
    + """  <section class="section">
    <div class="wrap">
      <div class="subpage-placeholder">
        <strong>Content pending</strong>
        This page will hold the full pricing detail (seat tiers, Manager Dashboard add-on, ROI calculator, and Investment in You ladder) once the homepage pricing display is simplified in Step 4 of the site restructure. Until then, see the full pricing section on the <a href="index.html#pricing">homepage</a>.
      </div>
    </div>
  </section>
"""
)
write_page(
    'pricing.html',
    'Pricing',
    'SOLVE Platform pricing: consultant seats, the optional Manager Dashboard, and your ROI.',
    pricing_body,
)

print('Done with content sub-pages.')
