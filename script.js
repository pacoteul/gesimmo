// Suppress AbortError for video play which can happen during scroll scrubbing
const originalPlay = HTMLMediaElement.prototype.play;
HTMLMediaElement.prototype.play = function() {
    const p = originalPlay.apply(this, arguments);
    if (p !== undefined) {
        p.catch(error => {
            if (error.name === 'AbortError') {
                // Silently ignore AbortError
                return;
            }
            throw error;
        });
    }
    return p;
};

// Initialize Lenis for Smooth Scrolling
const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    direction: 'vertical',
    gestureDirection: 'vertical',
    smooth: true,
    mouseMultiplier: 1,
    smoothTouch: false,
    touchMultiplier: 2,
    infinite: false,
});

// Update Lenis on requestAnimationFrame
function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
}
requestAnimationFrame(raf);

// Fixed Logo & Scroll Magic Elements
const logo = document.getElementById('logo');
const headerNav = document.getElementById('header-nav');
const parallaxBg = document.querySelector('.parallax-bg');
const imageSection = document.querySelector('.image-section');
const heroVideo = document.getElementById('hero-video');
const content1 = document.getElementById('hero-content-1');
const content2 = document.getElementById('hero-content-2');

let videoDuration = 0;
if (heroVideo) {
    // Make sure we have the duration of the video
    if (heroVideo.readyState >= 1) {
        videoDuration = heroVideo.duration;
    } else {
        heroVideo.addEventListener('loadedmetadata', () => {
            videoDuration = heroVideo.duration;
        });
    }
}

const locationVideo = document.getElementById('location-video');
let locationDuration = 0;
if (locationVideo) {
    if (locationVideo.readyState >= 1) {
        locationDuration = locationVideo.duration;
    } else {
        locationVideo.addEventListener('loadedmetadata', () => {
            locationDuration = locationVideo.duration;
        });
    }
}

const gestionVideo = document.getElementById('gestion-video');
let gestionDuration = 0;
if (gestionVideo) {
    if (gestionVideo.readyState >= 1) {
        gestionDuration = gestionVideo.duration;
    } else {
        gestionVideo.addEventListener('loadedmetadata', () => {
            gestionDuration = gestionVideo.duration;
        });
    }
}

function updateScrollEffects() {
    // 0. Unified Video Scrubbing based on main scroll section
    const mainSection = document.getElementById('main-scroll');
    if (mainSection) {
        const rect = mainSection.getBoundingClientRect();
        // total scrollable height = 1200vh - 100vh = 1100vh
        const maxScroll = rect.height - window.innerHeight;
        
        let scrollProgress = 0;
        if (rect.top <= 0) {
            scrollProgress = Math.abs(rect.top) / maxScroll;
        }
        scrollProgress = Math.max(0, Math.min(scrollProgress, 0.9999));

        const container1 = document.getElementById('video-container-1');
        const container2 = document.getElementById('video-container-2');
        const container3 = document.getElementById('video-container-3');

        // First third of scroll (0 to 0.333) is Video 1
        if (scrollProgress < 0.333) {
            if (container1) { container1.style.opacity = 1; container1.style.pointerEvents = 'auto'; }
            if (container2) { container2.style.opacity = 0; container2.style.pointerEvents = 'none'; }
            if (container3) { container3.style.opacity = 0; container3.style.pointerEvents = 'none'; }
            
            // Map 0 -> 0.333 to 0 -> 1 for video 1
            let v1Progress = scrollProgress * 3;
            if (heroVideo && videoDuration > 0) heroVideo.currentTime = videoDuration * v1Progress;
            
            // Toggle text at 1 second
            if (heroVideo && heroVideo.currentTime >= 1) {
                if (content1) content1.classList.add('hidden');
                if (content2) content2.classList.add('visible');
            } else {
                if (content1) content1.classList.remove('hidden');
                if (content2) content2.classList.remove('visible');
            }
        } 
        // Second third of scroll (0.333 to 0.666) is Video 2
        else if (scrollProgress >= 0.333 && scrollProgress < 0.666) {
            if (container1) { container1.style.opacity = 0; container1.style.pointerEvents = 'none'; }
            if (container2) { container2.style.opacity = 1; container2.style.pointerEvents = 'auto'; }
            if (container3) { container3.style.opacity = 0; container3.style.pointerEvents = 'none'; }
            
            // Map 0.333 -> 0.666 to 0 -> 1 for video 2
            let v2Progress = (scrollProgress - 0.333) * 3;
            if (locationVideo && locationDuration > 0) locationVideo.currentTime = locationDuration * v2Progress;
        }
        // Last third of scroll (0.666 to 1.0) is Video 3
        else {
            if (container1) { container1.style.opacity = 0; container1.style.pointerEvents = 'none'; }
            if (container2) { container2.style.opacity = 0; container2.style.pointerEvents = 'none'; }
            if (container3) { container3.style.opacity = 1; container3.style.pointerEvents = 'auto'; }
            
            // Map 0.666 -> 1.0 to 0 -> 1 for video 3
            let v3Progress = (scrollProgress - 0.666) * 3;
            if (gestionVideo && gestionDuration > 0) gestionVideo.currentTime = gestionDuration * v3Progress;
        }
    }

    // 1. Logo and Nav Background Check
    if (logo) {
        // Find the center of the logo
        const rect = logo.getBoundingClientRect();
        const logoCenterX = rect.left + rect.width / 2;
        const logoCenterY = rect.top + rect.height / 2;
        
        // Temporarily hide to check what's underneath
        logo.style.visibility = 'hidden';
        if (headerNav) headerNav.style.visibility = 'hidden';
        
        const elemBelow = document.elementFromPoint(logoCenterX, logoCenterY);
        
        logo.style.visibility = 'visible';
        if (headerNav) headerNav.style.visibility = 'visible';

        if (elemBelow) {
            // Find the closest section to determine the theme (dark or light)
            const section = elemBelow.closest('section');
            if (section) {
                if (section.classList.contains('light')) {
                    // On light backgrounds, invert the white logo and nav to make them black
                    logo.classList.add('invert');
                    if (headerNav) headerNav.classList.add('invert');
                } else if (section.classList.contains('dark')) {
                    // On dark backgrounds, keep them white as is
                    logo.classList.remove('invert');
                    if (headerNav) headerNav.classList.remove('invert');
                }
            }
        }
    }

    // 2. Parallax Effect for the Image Section
    if (parallaxBg && imageSection) {
        const rect = imageSection.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        
        // Check if the image section is in the viewport
        if (rect.top < windowHeight && rect.bottom > 0) {
            // Calculate progress of section through viewport (0 to 1)
            const progress = (windowHeight - rect.top) / (windowHeight + rect.height);
            
            // Move background: negative offset for upward parallax
            // Adjust the multiplier (30%) for more or less parallax intensity
            parallaxBg.style.transform = `translateY(${(progress - 0.5) * 30}%)`;
        }
    }
}

// Attach the update function to the Lenis scroll event
lenis.on('scroll', updateScrollEffects);

// Also check on load and resize
window.addEventListener('load', updateScrollEffects);
window.addEventListener('resize', updateScrollEffects);

// Expose lenis globally for the CTA button onclick
window.lenis = lenis;

// =========================================
// Text Reveal Animation
// =========================================
const revealElements = document.querySelectorAll('.reveal-text');

revealElements.forEach(el => {
    const text = el.innerText;
    el.innerHTML = '';
    const words = text.split(' ');
    words.forEach(word => {
        const span = document.createElement('span');
        span.innerHTML = word + '&nbsp;';
        span.style.opacity = '0.15';
        span.style.transition = 'opacity 0.4s ease, transform 0.4s ease, color 0.4s ease';
        span.style.display = 'inline-block';
        span.style.transform = 'translateY(15px)';
        el.appendChild(span);
    });
});

function updateTextReveal() {
    revealElements.forEach(el => {
        const rect = el.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        
        // Element is visible in viewport
        if (rect.top < windowHeight && rect.bottom > 0) {
            let progress = (windowHeight - rect.top) / (windowHeight * 0.7);
            progress = Math.max(0, Math.min(progress, 1));
            
            const spans = el.querySelectorAll('span');
            const total = spans.length;
            const revealCount = Math.floor(progress * total);
            
            spans.forEach((span, index) => {
                if (index < revealCount) {
                    span.style.opacity = '1';
                    span.style.transform = 'translateY(0)';
                    span.style.color = 'var(--primary)'; // Highlights with gold color
                } else {
                    span.style.opacity = '0.15';
                    span.style.transform = 'translateY(15px)';
                    span.style.color = 'var(--text-dark)';
                }
            });
        }
    });
}

// Ensure updateTextReveal is called on scroll and load
lenis.on('scroll', updateTextReveal);
window.addEventListener('load', updateTextReveal);
window.addEventListener('resize', updateTextReveal);
updateTextReveal();
