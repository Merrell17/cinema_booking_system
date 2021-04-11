// Nav bar slide out
const slide_out = () => {
    const site_link_li = document.querySelectorAll('.site-link li')
    const nav = document.querySelector('.site-link')
    const hamburger = document.querySelector('.hamburger');

    hamburger.addEventListener('click', ()=> {
        nav.classList.toggle('slide-nav');


    });

    var small_screen = window.matchMedia("(max-width: 900px)")
    if (small_screen.matches) {
        site_link_li.forEach((nav_link) => {
            nav_link.style.animation = `nav-links-slide 0.5s ease forwards`;
        });

    // Create ripple effect
    } else {
        site_link_li.forEach((nav_link, count) => {
            nav_link.style.animation = `nav-links-slide 0.5s ease forwards ${count / 8}s`;
        });
    }
}
slide_out();