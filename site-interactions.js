(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.add('js-motion');

  const revealTargets = document.querySelectorAll([
    '.hero > div',
    'section > .section-title',
    '.journey-intro',
    '.timeline-item',
    '.contact > .card',
    '.capability-list > li',
    '.featured-grid > a',
    '.project-grid > .project-card',
    '.certificate-grid > .certificate-card'
  ].join(','));

  revealTargets.forEach((target) => target.classList.add('reveal'));
  if (reduceMotion || !('IntersectionObserver' in window)) {
    revealTargets.forEach((target) => target.classList.add('is-visible'));
  } else {
    const observer = new IntersectionObserver((entries, activeObserver) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        activeObserver.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    revealTargets.forEach((target) => observer.observe(target));
  }

  const interactiveCards = document.querySelectorAll('.journey-card, .project-card, .featured-card, .capability-list > li, .certificate-card');
  interactiveCards.forEach((card) => {
    card.classList.add('interactive-card');
    card.addEventListener('pointermove', (event) => {
      if (event.pointerType === 'touch') return;
      const bounds = card.getBoundingClientRect();
      card.style.setProperty('--pointer-x', `${event.clientX - bounds.left}px`);
      card.style.setProperty('--pointer-y', `${event.clientY - bounds.top}px`);
    });
  });

  const progress = document.createElement('div');
  progress.className = 'scroll-progress';
  progress.setAttribute('aria-hidden', 'true');
  document.body.prepend(progress);

  const topButton = document.createElement('button');
  topButton.className = 'back-to-top';
  topButton.type = 'button';
  topButton.setAttribute('aria-label', '回到頁首');
  topButton.innerHTML = '<span aria-hidden="true">↑</span>';
  document.body.append(topButton);
  topButton.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }));

  const updateScrollUI = () => {
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = maxScroll > 0 ? Math.min(window.scrollY / maxScroll, 1) : 0;
    progress.style.transform = `scaleX(${ratio})`;
    topButton.classList.toggle('is-visible', window.scrollY > 420);
  };
  window.addEventListener('scroll', updateScrollUI, { passive: true });
  window.addEventListener('resize', updateScrollUI);
  updateScrollUI();
})();

