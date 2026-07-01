/**
 * KY Food Delivery System
 * Component: Footer
 *
 * The site-wide footer with brand info, navigation columns, and legal row.
 *
 * @param {Object}   options
 * @param {string}   [options.logoSrc]    - Logo image path
 * @param {string}   [options.tagline]    - Brand tagline text
 * @param {Array}    [options.columns]    - Array of { heading, links: [{ label, href }] }
 * @param {string}   [options.copyright]  - Copyright text (auto-generated if omitted)
 * @param {Array}    [options.legalLinks] - Array of { label, href } for legal row
 * @param {string}   [options.className]  - Extra CSS classes
 * @returns {HTMLElement} <footer> element
 */

export function Footer({
  logoSrc = null,
  tagline = 'Bold flavour. Fast delivery. Always KY.',
  columns = [],
  copyright = null,
  legalLinks = [],
  className = '',
} = {}) {
  const footer = document.createElement('footer');
  footer.className = ['footer', className].filter(Boolean).join(' ');

  // ── Top section ───────────────────────────────────────────────────────────
  const top = document.createElement('div');
  top.className = 'footer__top';

  // Brand column
  const brand = document.createElement('div');
  brand.className = 'footer__brand';

  if (logoSrc) {
    const logo = document.createElement('img');
    logo.src = logoSrc;
    logo.alt = 'KY Foods logo';
    logo.className = 'footer__logo';
    brand.appendChild(logo);
  } else {
    const wordmark = document.createElement('span');
    wordmark.className = 'footer__wordmark';
    wordmark.textContent = 'KY Foods';
    brand.appendChild(wordmark);
  }

  const taglineEl = document.createElement('p');
  taglineEl.className = 'footer__tagline';
  taglineEl.textContent = tagline;
  brand.appendChild(taglineEl);

  top.appendChild(brand);

  // Nav columns
  columns.forEach(({ heading, links = [] }) => {
    const col = document.createElement('div');
    col.className = 'footer__col';

    const h = document.createElement('h3');
    h.className = 'footer__col-heading';
    h.textContent = heading;
    col.appendChild(h);

    const ul = document.createElement('ul');
    ul.className = 'footer__col-links';
    ul.setAttribute('role', 'list');

    links.forEach(({ label, href = '#' }) => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = href;
      a.className = 'footer__link';
      a.textContent = label;
      li.appendChild(a);
      ul.appendChild(li);
    });

    col.appendChild(ul);
    top.appendChild(col);
  });

  footer.appendChild(top);

  // ── Divider ───────────────────────────────────────────────────────────────
  const divider = document.createElement('hr');
  divider.className = 'footer__divider';
  footer.appendChild(divider);

  // ── Bottom row ────────────────────────────────────────────────────────────
  const bottom = document.createElement('div');
  bottom.className = 'footer__bottom';

  const year = new Date().getFullYear();
  const copyrightEl = document.createElement('span');
  copyrightEl.className = 'footer__copyright';
  copyrightEl.textContent = copyright || `${year} KY Foods. All rights reserved.`;
  bottom.appendChild(copyrightEl);

  if (legalLinks.length) {
    const legalNav = document.createElement('nav');
    legalNav.setAttribute('aria-label', 'Legal links');
    const ul = document.createElement('ul');
    ul.className = 'footer__legal-links';
    ul.setAttribute('role', 'list');

    legalLinks.forEach(({ label, href = '#' }) => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = href;
      a.className = 'footer__link footer__link--legal';
      a.textContent = label;
      li.appendChild(a);
      ul.appendChild(li);
    });

    legalNav.appendChild(ul);
    bottom.appendChild(legalNav);
  }

  footer.appendChild(bottom);

  return footer;
}
