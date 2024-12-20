const toggleThemeButton = document.getElementById('toggle-theme');
const sectionElements = document.querySelectorAll('section');
const isDesktop = window.innerWidth >= 768;
const menuClass = isDesktop ? '.menu--desktop' : '.menu--mobile';
const linkElements = document.querySelectorAll(`${menuClass} .menu__link`);

// carrega tema do local storage se houver (default dark)
let theme = localStorage.getItem('theme') || 'dark';

function initToggleButton() {
  const initialButtonIcon = (theme === 'dark' ? 'bi-sun' : 'bi-moon-stars');
  toggleThemeButton.classList.add(initialButtonIcon);
  toggleThemeButton.addEventListener('click', changeTheme);
}

function updateTheme() {
  document.documentElement.dataset.theme = theme;
  localStorage.setItem('theme', theme);
}

function changeTheme() {
  theme = (theme === 'dark' ? 'light' : 'dark');
  toggleThemeButton.classList.toggle('bi-sun');
  toggleThemeButton.classList.toggle('bi-moon-stars');
  updateTheme();
}

function clearActive() {
  linkElements.forEach((link) => {
    link.classList.remove('active');
  });
}

function initMenu() {
  let ignoreScroll = false;
  let scrollTimeOut = null;

  linkElements.forEach((link) => {
    link.addEventListener('click', () => {
      clearTimeout(scrollTimeOut);
      ignoreScroll = true;

      clearActive();
      link.classList.add('active');
      scrollTimeOut = setTimeout(() => ignoreScroll = false, 1000);
    });
  });

  window.addEventListener('scroll', () => {
    if (ignoreScroll) return;
    const scrollPosition = Math.ceil(window.scrollY) + 50;

    sectionElements.forEach(section => {
      const sectionPosition = section.offsetTop;
      const sectionHeight = section.offsetHeight;

      if (scrollPosition >= sectionPosition && scrollPosition < (sectionPosition + sectionHeight)) {
        clearActive();
        document.querySelector(`${menuClass} a[href="#${section.id}"]`).classList.add('active');
      }
    });
  });
}

// atualiza a página para mudar o menu
window.onresize = () => ((window.innerWidth >= 768) != isDesktop) && location.reload();
window.onbeforeunload = () => window.scrollTo(0, 0);

updateTheme();
initToggleButton();
initMenu();