document.addEventListener('DOMContentLoaded', () => {
    window.addEventListener('load', () => {
        document.body.classList.add('loaded');
    });

    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('open');
            const isOpen = mobileMenu.classList.contains('open');
            mobileMenuBtn.innerHTML = isOpen ? '<i class="ph ph-x"></i>' : '<i class="ph ph-list"></i>';
        });
        // Close on link click
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('open');
                mobileMenuBtn.innerHTML = '<i class="ph ph-list"></i>';
            });
        });
    }

    // Disable custom cursor on touch devices
    if ('ontouchstart' in window) {
        const cursor = document.getElementById('indoor-cursor');
        if (cursor) cursor.style.display = 'none';
        const wrapper = document.querySelector('.indoor-carousel-wrapper');
        if (wrapper) wrapper.style.cursor = 'grab';
    }

    // 1. Hero Effects
    const heroBg = document.querySelector('.hero-bg video, .hero-bg img');
    const heroTitle = document.querySelector('.main-title');

    // 2. Philosophy Logic (5 Scenes)
    const pSection = document.getElementById('philosophy');
    const scene1 = document.querySelector('.scene-1');
    const scene2 = document.querySelector('.scene-2');
    const scene3 = document.querySelector('.scene-3');
    const scene4 = document.querySelector('.scene-4');

    // 3. Horizontal Scroll Logic
    const hSection = document.querySelector('.horizontal-scroll-section');
    const hWrapper = document.querySelector('.sticky-wrapper-horizontal');
    const hTrack = document.querySelector('.horizontal-track');

    // Set initial card states for reveal animation
    if (hTrack) {
        const initCards = hTrack.querySelectorAll('.treatment-item');
        initCards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(40px)';
            card.style.transition = 'all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        });
    }

    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;

        // HERO Scaling
        if (scrollY < window.innerHeight * 1.5) {
            const progress = scrollY / window.innerHeight;
            if (heroBg) heroBg.style.transform = `scale(${1 + progress * 0.2})`;
            if (heroTitle) {
                heroTitle.style.opacity = `${1 - progress * 1.5}`;
                heroTitle.style.transform = `translate(-50%, calc(-50% - ${scrollY * 0.5}px))`;
            }
        }

        // PHILOSOPHY Switch (5 Scenes)
        if (pSection && scene1 && scene2 && scene3 && scene4) {
            const rect = pSection.getBoundingClientRect();
            const sectionHeight = pSection.offsetHeight;
            const viewportHeight = window.innerHeight;
            const scrollDist = -rect.top;
            const totalScroll = sectionHeight - viewportHeight;
            let progress = scrollDist / totalScroll;

            if (progress < 0) progress = 0; if (progress > 1) progress = 1;

            const allScenes = [scene1, scene2, scene3, scene4];
            allScenes.forEach(s => s.classList.remove('active'));

            if (progress < 0.25) {
                scene1.classList.add('active');
            } else if (progress < 0.5) {
                scene2.classList.add('active');
            } else if (progress < 0.75) {
                scene3.classList.add('active');
            } else {
                scene4.classList.add('active');
            }
        }

        // HORIZONTAL SCROLL
        if (hSection && hWrapper && hTrack && window.innerWidth > 1024) {
            const sectionTop = hSection.offsetTop;
            const sectionHeight = hSection.offsetHeight;
            const viewportHeight = window.innerHeight;

            const distance = scrollY - sectionTop;
            const maxDistance = sectionHeight - viewportHeight;
            let percentage = distance / maxDistance;

            if (percentage < 0) percentage = 0; if (percentage > 1) percentage = 1;

            const trackWidth = hTrack.scrollWidth;
            const moveAmt = (trackWidth - window.innerWidth) * percentage;
            hTrack.style.transform = `translateX(-${moveAmt}px)`;

            // Progress bar update
            const progressBar = document.querySelector('.scroll-progress-bar');
            if (progressBar) {
                progressBar.style.width = `${percentage * 100}%`;
            }

            // Card reveal animation based on scroll
            const cards = hTrack.querySelectorAll('.treatment-item');
            cards.forEach((card, i) => {
                const cardLeft = card.offsetLeft;
                const visiblePoint = moveAmt + window.innerWidth * 0.8;
                if (cardLeft < visiblePoint) {
                    card.style.opacity = '1';
                    card.style.transform = card.matches(':hover') ? 'translateY(-12px)' : 'translateY(0)';
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(40px)';
                }
            });
        }

        // MEDIA SECTIONS (Shorts & TV) - now standalone sections, no scroll logic needed
    });

    // 4. B&A Centered Logic (Tabs, Max 4 Items)
    const bnaTrack = document.getElementById('bna-track');
    const bnaTabs = document.querySelectorAll('.tab-btn-center');

    // Animation Observer
    const bnaObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                document.querySelector('.bna-header').classList.add('visible');
                document.querySelector('.bna-slider-area').classList.add('visible');
                document.querySelector('.bna-bottom-area').classList.add('visible');
            }
        });
    }, { threshold: 0.3 });
    const bnaSection = document.getElementById('bna');
    if (bnaSection) bnaObserver.observe(bnaSection);

    // Generator (Split Slides) - Uses actual B&A images from subpage folders
    // Auto-Scroll Logic Variable
    let bnaAutoScrollInterval;

    // B&A Image data per category (actual project images)
    const bnaImageData = {
        whitening: [
            { src: '/images/main/unnamed (1).png' },
            { src: '/images/main/unnamed (2).png' },
            { src: '/images/main/unnamed (3).png' },
            { src: '/images/main/unnamed (4).png' },
            { src: '/images/main/unnamed (5).png' },
            { src: '/images/main/unnamed (6).png' },
            { src: '/images/main/unnamed (7).png' }
        ],
        laminate: [
            { src: '/images/main/unnamed (8).png' },
            { src: '/images/main/unnamed (9).png' },
            { src: '/images/main/unnamed (10).png' },
            { src: '/images/main/unnamed (11).png' },
            { src: '/images/main/unnamed (12).png' }
        ],
        orthodontics: [
            { src: '/images/main/unnamed (13).png' },
            { src: '/images/main/unnamed (14).png' },
            { src: '/images/main/unnamed (15).png' },
            { src: '/images/main/unnamed (16).png' },
            { src: '/images/main/unnamed (17).png' },
            { src: '/images/main/unnamed (18).png' }
        ],
        implant: [
            { src: '/images/main/unnamed (19).png' },
            { src: '/images/main/unnamed (20).png' },
            { src: '/images/main/unnamed (21).png' },
            { src: '/images/main/unnamed (22).png' }
        ]
    };

    const generateBnaItems = (category) => {
        let html = '';
        const images = bnaImageData[category] || bnaImageData['whitening'];

        images.forEach((item, idx) => {
            const caseNum = idx + 1;
            const caseLabel = 'CASE ' + String(caseNum).padStart(2, '0');
            html += `
            <div class="bna-slide-item">
                <span class="bna-case-num">${caseLabel}</span>
                <img src="${item.src}" alt="Case ${caseNum}">
            </div>`;
        });

        const totalEl = document.getElementById('bna-total');
        if (totalEl) totalEl.textContent = String(images.length).padStart(2, '0');
        const currentEl = document.getElementById('bna-current');
        if (currentEl) currentEl.textContent = '01';

        return html;
    };

    const startBnaAutoScrollStrict = () => {
        if (bnaAutoScrollInterval) clearInterval(bnaAutoScrollInterval);
        const slider = document.querySelector('.bna-slider-area');
        if (!slider) return;

        bnaAutoScrollInterval = setInterval(() => {
            const item = slider.querySelector('.bna-slide-item');
            if (!item) return;
            // Calculate width dynamically
            const style = window.getComputedStyle(slider.querySelector('.bna-track-center'));
            const gap = parseFloat(style.gap) || 20;
            const itemWidth = item.offsetWidth + gap;

            const maxScroll = slider.scrollWidth - slider.clientWidth;

            // Slide 2 items (bundle) at a time
            if (Math.ceil(slider.scrollLeft) >= maxScroll - 5) {
                slider.scrollTo({ left: 0, behavior: 'smooth' });
            } else {
                slider.scrollBy({ left: itemWidth * 2, behavior: 'smooth' });
            }
        }, 3000); // 3 seconds (Slower)
    };

    if (bnaTrack) {
        bnaTrack.innerHTML = generateBnaItems('whitening'); // Default category
        startBnaAutoScrollStrict();
    }

    // B&A Navigation Buttons
    const bnaPrev = document.querySelector('.bna-prev');
    const bnaNext = document.querySelector('.bna-next');

    const updateBnaCounter = () => {
        const slider = document.querySelector('.bna-slider-area');
        if (!slider) return;
        const items = slider.querySelectorAll('.bna-slide-item');
        if (!items.length) return;
        const style = window.getComputedStyle(slider.querySelector('.bna-track-center'));
        const gap = parseFloat(style.gap) || 20;
        const itemWidth = items[0].offsetWidth + gap;
        const scrollPos = slider.scrollLeft;
        // Each case is 2 items (before/after pair)
        const visibleIdx = Math.round(scrollPos / itemWidth);
        const currentEl = document.getElementById('bna-current');
        if (currentEl) currentEl.textContent = String(visibleIdx + 1).padStart(2, '0');
    };

    // Update counter on scroll
    const bnaSlider = document.querySelector('.bna-slider-area');
    if (bnaSlider) {
        bnaSlider.addEventListener('scroll', () => {
            requestAnimationFrame(updateBnaCounter);
        });
    }

    if (bnaPrev && bnaNext) {
        bnaPrev.addEventListener('click', () => {
            const slider = document.querySelector('.bna-slider-area');
            if (!slider) return;
            const item = slider.querySelector('.bna-slide-item');
            if (!item) return;
            const style = window.getComputedStyle(slider.querySelector('.bna-track-center'));
            const gap = parseFloat(style.gap) || 20;
            const itemWidth = item.offsetWidth + gap;

            if (slider.scrollLeft <= 5) {
                slider.scrollTo({ left: slider.scrollWidth - slider.clientWidth, behavior: 'smooth' });
            } else {
                slider.scrollBy({ left: -(itemWidth * 2), behavior: 'smooth' });
            }
            startBnaAutoScrollStrict();
        });
        bnaNext.addEventListener('click', () => {
            const slider = document.querySelector('.bna-slider-area');
            if (!slider) return;
            const item = slider.querySelector('.bna-slide-item');
            if (!item) return;
            const style = window.getComputedStyle(slider.querySelector('.bna-track-center'));
            const gap = parseFloat(style.gap) || 20;
            const itemWidth = item.offsetWidth + gap;

            const maxScroll = slider.scrollWidth - slider.clientWidth;
            if (Math.ceil(slider.scrollLeft) >= maxScroll - 5) {
                slider.scrollTo({ left: 0, behavior: 'smooth' });
            } else {
                slider.scrollBy({ left: (itemWidth * 2), behavior: 'smooth' });
            }
            startBnaAutoScrollStrict();
        });
    }

    // Tabs Click
    bnaTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            bnaTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const cat = tab.getAttribute('data-tab');
            if (bnaTrack) {
                bnaTrack.style.opacity = 0;
                bnaTrack.style.transform = 'translateY(20px)';
                clearInterval(bnaAutoScrollInterval); // Stop

                setTimeout(() => {
                    bnaTrack.innerHTML = generateBnaItems(cat);
                    bnaTrack.style.opacity = 1;
                    bnaTrack.style.transform = 'translateY(0)';
                    startBnaAutoScrollStrict(); // Restart
                }, 300);
            }
        });
    });

    // 5. SHORTS Marquee (duplicate existing HTML cards for seamless loop)
    const shortsTrack = document.getElementById('shorts-track');
    if (shortsTrack) {
        // Duplicate existing cards for marquee seamless loop
        const originalCards = shortsTrack.innerHTML;
        shortsTrack.innerHTML = originalCards + originalCards;
    }

    // Shorts Navigation Buttons
    const shortsPrev = document.getElementById('shorts-prev');
    const shortsNext = document.getElementById('shorts-next');
    const shortsWrapper = document.querySelector('.shorts-slider-wrapper');

    if (shortsPrev && shortsNext && shortsWrapper) {
        const scrollAmount = 620; // 2 cards worth (280px + 30px gap) * 2

        const shortsScroll = (direction) => {
            const track = document.getElementById('shorts-track');
            if (track) track.style.animationPlayState = 'paused';
            shortsWrapper.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
            setTimeout(() => {
                if (track) track.style.animationPlayState = 'running';
            }, 3000);
        };

        shortsPrev.addEventListener('click', () => shortsScroll(-1));
        shortsNext.addEventListener('click', () => shortsScroll(1));
    }

    // 6. YouTube Slider (3 Items View, Loop, 1-item Move)
    const ytTrack = document.getElementById('yt-track');
    const ytPrevBtn = document.getElementById('yt-prev');
    const ytNextBtn = document.getElementById('yt-next');

    // Use existing HTML cards (no mock data generation)
    if (ytTrack) {
        // Slider Logic (3 Items View, Loop with actual cards)
        let currentIdx = 0;
        const totalItems = ytTrack.querySelectorAll('.yt-card').length;
        const viewCount = 3;

        const updateSlider = () => {
            // Move 1 item at a time = 33.333% (since item is 33.333% width)
            const percentage = currentIdx * 33.3333;
            ytTrack.style.transform = `translateX(-${percentage}%)`;
        };

        if (ytNextBtn) {
            ytNextBtn.addEventListener('click', () => {
                if (currentIdx < totalItems - viewCount) {
                    currentIdx++;
                } else {
                    currentIdx = 0; // Loop back to start
                }
                updateSlider();
            });
        }
        if (ytPrevBtn) {
            ytPrevBtn.addEventListener('click', () => {
                if (currentIdx > 0) {
                    currentIdx--;
                } else {
                    currentIdx = totalItems - viewCount; // Loop to end
                }
                updateSlider();
            });
        }
    }
    // 7. Review Slider (Infinite Loop, 3 items view, Step-by-step)
    const reviewTrack = document.querySelector('.review-track');
    if (reviewTrack) {
        const originalCards = reviewTrack.querySelectorAll('.review-card');
        const cardCount = originalCards.length; // 6
        const viewCount = 3;
        const gap = 30; // matches CSS gap

        // Clone first 'viewCount' items to end for infinite loop illusion
        if (cardCount >= viewCount) {
            for (let i = 0; i < viewCount; i++) {
                const clone = originalCards[i].cloneNode(true);
                clone.classList.add('clone');
                reviewTrack.appendChild(clone);
            }
        }

        let rIndex = 0;
        let isTransitioning = false;

        // Auto Slide Function
        const slideReview = () => {
            if (isTransitioning) return;
            const firstCard = reviewTrack.querySelector('.review-card');
            if (!firstCard) return;

            isTransitioning = true;
            rIndex++;
            reviewTrack.style.transition = 'transform 0.5s cubic-bezier(0.25, 1, 0.5, 1)';

            const itemWidth = firstCard.offsetWidth + gap;
            reviewTrack.style.transform = `translateX(-${rIndex * itemWidth}px)`;
        };

        // Transition End -> Reset if needed
        reviewTrack.addEventListener('transitionend', () => {
            isTransitioning = false;
            // If we reached the clone start (index 6, which looks like index 0)
            if (rIndex >= cardCount) {
                reviewTrack.style.transition = 'none';
                rIndex = 0;
                reviewTrack.style.transform = `translateX(0)`;
            }
        });

        // Interval
        setInterval(slideReview, 3000);

        // Recalculate on Resize (Reset)
        window.addEventListener('resize', () => {
            reviewTrack.style.transition = 'none';
            rIndex = 0;
            reviewTrack.style.transform = `translateX(0)`;
        });
    }
    // 5. INDOOR SPACES (Apgujeong)
    const indoorTrack = document.getElementById('indoor-track');
    const indoorCursor = document.getElementById('indoor-cursor');
    const indoorSection = document.getElementById('indoor-spaces');
    const indoorTabs = document.querySelectorAll('.indoor-tab');

    // All indoor images flattened into a single array
    const indoorAllImages = [
        '/images/main/다운로드.jpg',
        '/images/main/다운로드.png',
        '/images/main/다운로드 (1).jpg',
        '/images/main/다운로드 (1).jpg',
        '/images/main/다운로드 (2).jpg',
        '/images/main/다운로드 (2).png',
        '/images/main/다운로드 (3).png'
    ];

    let isIndDragging = false;
    let indStartX, indScrollLeft;

    // Render Function (all images, no category)
    const renderIndoorItems = () => {
        if (!indoorTrack) return;
        indoorTrack.innerHTML = '';
        const images = indoorAllImages;
        const total = images.length;

        // Update Total Counter
        const totalEl = document.getElementById('i-total');
        if (totalEl) totalEl.textContent = total;

        // Duplicate images for infinite feel
        const displayImages = [];
        const repeatCount = 3; // minimal repeat

        for (let r = 0; r < repeatCount; r++) {
            images.forEach((url, idx) => {
                displayImages.push({ url, index: idx + 1 });
            });
        }

        displayImages.forEach(item => {
            const div = document.createElement('div');
            div.className = 'indoor-item';
            div.dataset.index = item.index; // Store original index (1~N)
            div.innerHTML = `<img src="${item.url}" alt="Indoor Space" draggable="false">`;
            indoorTrack.appendChild(div);
        });

        // Center the scroll initially (middle set)
        const indoorWrapper = document.querySelector('.indoor-carousel-wrapper');
        if (indoorWrapper) {
            // Wait for render
            setTimeout(() => {
                const trackWidth = indoorTrack.scrollWidth;
                indoorWrapper.scrollLeft = (trackWidth / 3) - (window.innerWidth / 2) + 250;
                updateIndoorCenter();
            }, 50);
        }
    };

    // Initialize (all images)
    renderIndoorItems();

    // Carousel Drag Logic
    const indoorWrapper = document.querySelector('.indoor-carousel-wrapper');
    if (indoorWrapper) {
        indoorWrapper.addEventListener('mousedown', (e) => {
            isIndDragging = true;
            indStartX = e.pageX - indoorWrapper.offsetLeft;
            indScrollLeft = indoorWrapper.scrollLeft;
            indoorWrapper.style.cursor = 'grabbing';
        });

        indoorWrapper.addEventListener('mouseleave', () => {
            isIndDragging = false;
            indoorWrapper.style.cursor = 'none';
        });
        indoorWrapper.addEventListener('mouseup', () => {
            isIndDragging = false;
            indoorWrapper.style.cursor = 'none';
        });

        indoorWrapper.addEventListener('mousemove', (e) => {
            if (!isIndDragging) return;
            e.preventDefault();
            const x = e.pageX - indoorWrapper.offsetLeft;
            const walk = (x - indStartX) * 1.5; // Scroll speed
            indoorWrapper.scrollLeft = indScrollLeft - walk;
            updateIndoorCenter();
        });

        // Touch support
        indoorWrapper.addEventListener('touchstart', (e) => {
            isIndDragging = true;
            indStartX = e.touches[0].pageX - indoorWrapper.offsetLeft;
            indScrollLeft = indoorWrapper.scrollLeft;
        });

        indoorWrapper.addEventListener('touchend', () => { isIndDragging = false; });

        indoorWrapper.addEventListener('touchmove', (e) => {
            if (!isIndDragging) return;
            const x = e.touches[0].pageX - indoorWrapper.offsetLeft;
            const walk = (x - indStartX) * 1.5;
            indoorWrapper.scrollLeft = indScrollLeft - walk;
            updateIndoorCenter();
        });

        // Center Check on Scroll
        indoorWrapper.addEventListener('scroll', () => {
            requestAnimationFrame(updateIndoorCenter);
        });
    }

    function updateIndoorCenter() {
        if (!indoorWrapper) return;
        const centerPoint = indoorWrapper.scrollLeft + (indoorWrapper.clientWidth / 2);
        const items = document.querySelectorAll('.indoor-item');

        let closestDist = Infinity;
        let closestItem = null;

        items.forEach(item => {
            const itemCenter = item.offsetLeft + (item.offsetWidth / 2);
            const dist = Math.abs(centerPoint - itemCenter);

            // If dragging close to center (threshold 250px)
            if (dist < 250) {
                item.classList.add('center');
            } else {
                item.classList.remove('center');
            }

            // Find closest for counter
            if (dist < closestDist) {
                closestDist = dist;
                closestItem = item;
            }
        });

        // Update Counter based on closest item
        if (closestItem) {
            const currentIdx = closestItem.dataset.index;
            const currentEl = document.getElementById('i-current');
            if (currentEl && currentIdx) currentEl.textContent = currentIdx;
        }
    }

    // Custom Cursor Logic
    if (indoorSection && indoorCursor) {
        indoorSection.addEventListener('mousemove', (e) => {
            const x = e.clientX;
            const y = e.clientY;
            indoorCursor.style.left = `${x}px`;
            indoorCursor.style.top = `${y}px`;
        });
    }

    // 8. Treatment Page Animation (Speciality & Panels)
    const specSection = document.querySelector('.speciality-section');
    if (specSection) {
        // Speciality Title & Cards Fade Up
        const specTitle = specSection.querySelector('.spec-title');
        const specCards = specSection.querySelectorAll('.spec-card');

        const specObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    if (entry.target.classList.contains('spec-title')) {
                        entry.target.classList.add('visible');
                    } else if (entry.target.classList.contains('spec-card')) {
                        entry.target.classList.add('visible');
                    }
                }
            });
        }, { threshold: 0.2 });

        if (specTitle) specObserver.observe(specTitle);
        specCards.forEach(card => specObserver.observe(card));
    }

    // Treatment Horizontal Panels Overlay Logic (Fade In content)
    const treatScroll = document.getElementById('treat-scroll');
    if (treatScroll) {
        const panels = treatScroll.querySelectorAll('.h-panel');
        // Simple trigger when in view (or use scroll progress if needed)
        const panelObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const content = entry.target.querySelector('.panel-content');
                    if (content) {
                        content.style.opacity = 1;
                        content.style.transform = 'translateY(0)';
                    }
                }
            });
        }, { threshold: 0.5 });

        panels.forEach(p => panelObserver.observe(p));
    }

    // 9. Global Fade-Up Observer (For Subpages)
    const fadeUpElements = document.querySelectorAll('.fade-up');
    if (fadeUpElements.length > 0) {
        const globalObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    // Optional: Stop observing once visible to run only once
                    // globalObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        fadeUpElements.forEach(el => globalObserver.observe(el));
    }

    // Section Title Entrance Animations
    const fadeTargets = document.querySelectorAll('.section-fade-up');
    if (fadeTargets.length > 0) {
        const fadeObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    fadeObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });
        fadeTargets.forEach(el => fadeObserver.observe(el));
    }
});
