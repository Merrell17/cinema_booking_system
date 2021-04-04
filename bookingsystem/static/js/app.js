// Nav bar slide out
const slide_out = () => {
    const site_link = document.querySelectorAll('.site-link li')
    const nav = document.querySelector('.site-link')
    const burger = document.querySelector('.burger');

    burger.addEventListener('click', ()=> {
        nav.classList.toggle('slide-nav');


    });

     site_link.forEach((nav_link, i) => {
        nav_link.style.animation = `nav-links-slide 0.5s ease forwards ${i/ 8}s`;

    });
}
slide_out();