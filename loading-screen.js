document.addEventListener("DOMContentLoaded", () => {
  // Create loading screen
  const loadingScreen = document.createElement("div");
  loadingScreen.id = "loading-screen";
  loadingScreen.style.position = "fixed";
  loadingScreen.style.top = "0";
  loadingScreen.style.left = "0";
  loadingScreen.style.width = "100%";
  loadingScreen.style.height = "100vh";
  loadingScreen.style.backgroundColor = "#0d0b09";
  loadingScreen.style.display = "flex";
  loadingScreen.style.justifyContent = "center";
  loadingScreen.style.alignItems = "center";
  loadingScreen.style.zIndex = "9999";
  loadingScreen.style.overflow = "hidden";

  // Circular gold halo behind the logo (round, so no square edges)
  const isPhone = window.innerWidth < 768;
  const halo = document.createElement("div");
  halo.className = "loading-halo";
  halo.style.position = "absolute";
  halo.style.width = isPhone ? "260px" : "380px";
  halo.style.height = isPhone ? "260px" : "380px";
  halo.style.borderRadius = "50%";
  halo.style.background = "radial-gradient(circle, rgba(242,193,78,.28) 0%, rgba(214,69,80,.12) 45%, transparent 70%)";
  halo.style.opacity = "0";
  halo.style.transform = "scale(.4)";
  loadingScreen.appendChild(halo);

  // Brand logo zooms in
  const logo = document.createElement("img");
  logo.src = "assets/logo.png";
  logo.style.width = isPhone ? "150px" : "220px";
  logo.style.height = "auto";
  logo.style.transform = "scale(0)";
  logo.style.position = "relative";
  logo.style.filter = "drop-shadow(0 18px 40px rgba(0,0,0,.65))";
  logo.className = "loading-logo";
  loadingScreen.appendChild(logo);

  // Disable scrolling
  document.body.style.overflow = "hidden";
  document.documentElement.style.overflow = "hidden";

  // Add loading screen to body
  document.body.appendChild(loadingScreen);

  // Halo blooms out, logo zooms in, then a gentle signature wiggle, slide away
  gsap.to(".loading-halo", {
    opacity: 1,
    scale: 1,
    duration: 1.1,
    ease: "power2.out",
  });
  gsap.to(".loading-logo", {
    scale: 1,
    duration: 0.75,
    ease: "power2.out",
    onComplete: () => {
      gsap.to(".loading-logo", {
        keyframes: [
          { rotation: -4, y: "-=8", duration: 0.5, ease: "power1.inOut" },
          { rotation: 4, y: "+=8", duration: 0.5, ease: "power1.inOut" },
          { rotation: -2, duration: 0.4, ease: "power1.inOut" },
          { rotation: 0, duration: 0.4, ease: "power1.inOut" },
        ],
        onComplete: () => {
          gsap.to(loadingScreen, {
            y: "-100%",
            duration: 1,
            ease: "power2.inOut",
            onComplete: () => {
              loadingScreen.remove();
              document.body.style.overflow = "";
              document.documentElement.style.overflow = "";
              // Page height changed while the screen was up — recalc Lenis + triggers
              if (window.__lenis) window.__lenis.resize();
              if (window.ScrollTrigger) ScrollTrigger.refresh();
            },
          });
        },
      });
    },
  });
});
