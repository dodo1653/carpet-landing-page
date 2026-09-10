// Lenis smooth scrolling, driven by GSAP's ticker so ScrollTrigger stays in sync
// (native touch scrolling on phones — Lenis sync makes mobile feel rubber-bandy)
const lenis = new Lenis({
  duration: 1.1,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smoothWheel: true,
  syncTouch: false,
});
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => {
  lenis.raf(time * 1000);
});
gsap.ticker.lagSmoothing(0);
window.__lenis = lenis;

// Recalculate Lenis's scroll limit once all images/fonts have loaded
// (it initializes while the loading screen is up, when the page is still short)
window.addEventListener('load', () => {
  lenis.resize();
  if (window.ScrollTrigger) ScrollTrigger.refresh();
});
// Mobile: browser chrome shows/hides and orientation flips change viewport height
window.addEventListener('orientationchange', () => {
  lenis.resize();
  if (window.ScrollTrigger) ScrollTrigger.refresh();
});

// Anchor links scroll through Lenis instead of jumping
 const anchors = document.querySelectorAll('a[href^="#"]');
anchors.forEach((a) => {
  a.addEventListener('click', (e) => {
    const id = a.getAttribute('href');
    if (id.length > 1 && document.querySelector(id)) {
      e.preventDefault();
      lenis.scrollTo(id, { offset: -80, duration: 1.4 });
    }
  });
});

gsap.registerPlugin(ScrollTrigger);

// "still aping alone?" scroll-scrubbed drift: desktop + tablet only. On phones the
// blocks become a static stacked list (CSS), so the scroll-jack is disabled entirely.
if (window.matchMedia('(min-width: 768px)').matches) {
  const isSmallScreen = window.innerWidth < 1300;

  // Add staggered delays to each block animation
  gsap.to(".block", {
    yPercent: isSmallScreen ? -200 : -900,
    scrollTrigger: {
      trigger: ".section-2",
      start: "top bottom",
      end: "bottom top",
      scrub: true,
    },
    ease: "none",
    delay: 0
  });

  gsap.to(".block-2", {
    yPercent: isSmallScreen ? -600 : -2700,
    scrollTrigger: {
      trigger: ".section-2",
      start: "top bottom",
      end: "bottom top",
      scrub: true,
    },
    ease: "none",
    delay: 0.2
  });

  gsap.to(".block-3", {
    yPercent: isSmallScreen ? -500 : -2300,
    scrollTrigger: {
      trigger: ".section-2",
      start: "top bottom",
      end: "bottom top",
      scrub: true,
    },
    ease: "none",
    delay: 0.4
  });

  gsap.to(".block-4", {
    yPercent: isSmallScreen ? -400 : -2000,
    scrollTrigger: {
      trigger: ".section-2",
      start: "top bottom",
      end: "bottom top",
      scrub: true,
    },
    ease: "none",
    delay: 0.6
  });

  gsap.to(".block-5", {
    yPercent: isSmallScreen ? -450 : -2100,
    scrollTrigger: {
      trigger: ".section-2",
      start: "top bottom",
      end: "bottom top",
      scrub: true,
    },
    ease: "none",
    delay: 0.8
  });

  gsap.to(".block-6", {
    yPercent: isSmallScreen ? -750 : -3750,
    scrollTrigger: {
      trigger: ".section-2",
      start: "top bottom",
      end: "bottom top",
      scrub: true,
    },
    ease: "none",
    delay: 1
  });
}

// Flying carpet spiral "wandering" animation on loop (no initial jump)
gsap.to(".image-4", {
  keyframes: [
    { x: "+=20", y: "-=10", rotation: "+=10", duration: 0.6, ease: "power1.inOut" },
    { x: "+=10", y: "+=20", rotation: "+=10", duration: 0.6, ease: "power1.inOut" },
    { x: "-=20", y: "+=10", rotation: "-=10", duration: 0.6, ease: "power1.inOut" },
    { x: "-=10", y: "-=20", rotation: "-=10", duration: 0.6, ease: "power1.inOut" }
  ],
  repeat: -1
});

// Feature cards: two counter-scrolling vertical marquees — seamless ticker loop.
// Wraps every frame via modulo and re-measures once fonts/images load, so there's
// no snap or restart flash at the loop point.
const colSetup = (col, dir) => {
  if (!col) return;
  Array.from(col.children).forEach((el) => {
    if (el.classList.contains('is-clone')) el.remove();
  });
  const cards = Array.from(col.children);
  cards.forEach((card) => {
    const clone = card.cloneNode(true);
    clone.classList.add('is-clone');
    col.appendChild(clone);
  });

  const GAP = 24;
  let total = 0;
  const measure = () => {
    total = cards.reduce((s, el) => s + el.offsetHeight + GAP, 0);
  };
  measure();
  window.addEventListener('load', measure);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
  window.addEventListener('resize', measure);

  let raw = 0; // accumulates; rendered value is wrapped into [-total, 0)
  gsap.ticker.add((time, delta) => {
    if (!total) return;
    raw += (dir === 'up' ? -1 : 1) * (delta / 1000) * 38; // px per second
    const wrapped = ((raw % total) + total) % total - total; // -total..0
    col.style.transform = 'translate3d(0,' + wrapped.toFixed(2) + 'px,0)';
  });
};
const cols = document.querySelectorAll('.features-col');
if (cols.length >= 2) {
  // Phones: single column drifting up. Tablet/desktop: two counter-scrolling columns.
  const isPhone = window.matchMedia('(max-width: 767px)').matches;
  if (isPhone) {
    colSetup(cols[0], 'up');
    cols[1].style.display = 'none';
  } else {
    colSetup(cols[0], 'up');
    colSetup(cols[1], 'down');
  }
  document.querySelectorAll('.features-marquee').forEach((m) => { m.style.overflow = 'hidden'; });
}

// Infinite horizontal loop for .pnls-line
const pnlsContainer = document.querySelector('.pnls-line');
const pnlsTrack = pnlsContainer ? pnlsContainer.querySelector('.pnls-track') : null;

if (pnlsTrack) {
  // Remove previous clones to avoid stacking
  Array.from(pnlsTrack.children).forEach(el => {
    if (el.classList.contains('is-clone')) el.remove();
  });

  // Duplicate all panel items for seamless looping
  const panels = Array.from(pnlsTrack.children);
  panels.forEach(panel => {
    const clone = panel.cloneNode(true);
    clone.classList.add('is-clone');
    pnlsTrack.appendChild(clone);
  });

  // Calculate total width of original panels (track uses a 10px flex gap, so add
  // one gap per panel — otherwise the loop seam shows a small skip)
  const GAP = 10;
  const panelWidths = panels.map(el => el.offsetWidth);
  const totalWidth = panelWidths.reduce((sum, w) => sum + w, 0) + GAP * panels.length;

  // Set track to row flex for horizontal stacking
  pnlsTrack.style.display = "flex";
  pnlsTrack.style.flexDirection = "row";
  pnlsTrack.style.flexWrap = "nowrap";

  // Animate the track leftward, looping seamlessly
  gsap.to(pnlsTrack, {
    x: -totalWidth,
    duration: panels.length * 2,
    ease: "none",
    repeat: -1,
    modifiers: {
      x: gsap.utils.unitize(x => parseFloat(x) % totalWidth)
    }
  });

  // Hide overflow on container
  pnlsContainer.style.overflow = "hidden";
}

// Carpet image animation (image-8): gentle bounce and tilt loop
gsap.to(".image-8", {
  keyframes: [
    { rotation: -10, duration: 0.8, ease: "power1.inOut" },
    { rotation: 8, duration: 0.8, ease: "power1.inOut" },
    { rotation: -5, duration: 0.8, ease: "power1.inOut" },
    { rotation: 6, duration: 0.8, ease: "power1.inOut" },
    { rotation: -10, duration: 0.8, ease: "power1.inOut" }
  ],
  repeat: -1
});

// Mobile menu (burger) — toggles the dropdown, closes on link tap
const burger = document.querySelector('.burger');
const options = document.querySelector('.options');
if (burger && options) {
  burger.addEventListener('click', () => {
    const open = options.classList.toggle('is-open');
    burger.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
  });
  options.querySelectorAll('a').forEach((a) => {
    a.addEventListener('click', () => {
      options.classList.remove('is-open');
      burger.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
    });
  });
}

// Showcase image: subtle parallax float
gsap.to(".image-showcase", {
  y: -30,
  scrollTrigger: {
    trigger: ".section-7",
    start: "top bottom",
    end: "bottom top",
    scrub: true,
  },
  ease: "none"
});

gsap.utils.toArray(".navbar img").forEach(logo => {
  logo.addEventListener("mouseenter", () => {
    gsap.to(logo, {
      rotation: 360,
      duration: 1.5,
      ease: "power2.inOut"
    });
  });
  logo.addEventListener("mouseleave", () => {
    gsap.to(logo, {
      rotation: 0,
      duration: 1.5,
      ease: "power2.inOut"
    });
  });
});
