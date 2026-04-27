// Year
document.getElementById('year').textContent = new Date().getFullYear();

// Mobile nav
const hamburger = document.getElementById('hamburger');
const navMobile = document.getElementById('nav-mobile');
hamburger.addEventListener('click', () => {
  navMobile.classList.toggle('open');
});
navMobile.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => navMobile.classList.remove('open'));
});

// Nav scroll shadow
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.style.boxShadow = window.scrollY > 10
    ? '0 4px 30px rgba(0,0,0,0.4)'
    : 'none';
}, { passive: true });

// Scroll reveal
const observer = new IntersectionObserver(
  entries => entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } }),
  { threshold: 0.12 }
);
document.querySelectorAll('.timeline-item, .project-card, .skill-group, .edu-card, .cert-card, .stat-card, .about-text, .contact-left, .contact-right').forEach(el => {
  el.classList.add('reveal');
  observer.observe(el);
});

// Terminal typing effect in hero
const typingCursor = document.getElementById('typing-cursor');
const phrases = [
  'build --outcome-driven-products',
  'ship --platform-at-scale',
  'lead --eng-biz-translation',
  'solve --hard-problems',
];
let phraseIdx = 0;
let charIdx = 0;
let deleting = false;

function type() {
  const current = phrases[phraseIdx];
  if (!deleting) {
    charIdx++;
    if (typingCursor) typingCursor.parentElement.innerHTML =
      `<span class="prompt">$</span> ${current.slice(0, charIdx)}<span id="typing-cursor" class="cursor-blink">█</span>`;
    if (charIdx === current.length) {
      deleting = true;
      setTimeout(type, 1800);
      return;
    }
  } else {
    charIdx--;
    if (typingCursor) typingCursor.parentElement.innerHTML =
      `<span class="prompt">$</span> ${current.slice(0, charIdx)}<span id="typing-cursor" class="cursor-blink">█</span>`;
    if (charIdx === 0) {
      deleting = false;
      phraseIdx = (phraseIdx + 1) % phrases.length;
    }
  }
  setTimeout(type, deleting ? 40 : 80);
}

setTimeout(type, 1200);
