document.addEventListener('DOMContentLoaded', function () {
  var mobileMenuButton = document.getElementById('mobile-menu-button');
  var mobileMenu = document.getElementById('mobile-menu');
  var navbar = document.querySelector('nav');

  if (mobileMenuButton && mobileMenu) {
    mobileMenuButton.addEventListener('click', function () {
      var expanded = this.getAttribute('aria-expanded') === 'true' ? false : true;
      this.setAttribute('aria-expanded', expanded);
      mobileMenu.classList.toggle('hidden');
      var icon = this.querySelector('i');
      if (icon) {
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-times');
      }
    });
  }

  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 50) {
        navbar.classList.add('bg-gray-900/80', 'backdrop-blur-xl');
        navbar.classList.remove('bg-transparent');
      } else {
        navbar.classList.remove('bg-gray-900/80', 'backdrop-blur-xl');
        navbar.classList.add('bg-transparent');
      }
    });
  }

  var scrollElements = document.querySelectorAll('.scroll-hidden');
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('scroll-visible');
        entry.target.classList.remove('scroll-hidden');
      }
    });
  }, {threshold: 0.1});
  scrollElements.forEach(function (el) { observer.observe(el); });
});
