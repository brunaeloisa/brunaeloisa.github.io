const toggleThemeButton = document.getElementById('toggle-theme');
const htmlElement = document.documentElement;
const linkElements = document.querySelectorAll('.menu__link');

function changeTheme() {
  const currentTheme = htmlElement.dataset.theme;
  htmlElement.dataset.theme = (currentTheme === 'dark' ? 'light' : 'dark');
  toggleThemeButton.classList.toggle('bi-sun');
  toggleThemeButton.classList.toggle('bi-moon-stars');
}

toggleThemeButton.addEventListener('click', changeTheme);

function clearActive() {
  linkElements.forEach((link) => {
    link.classList.remove('active');
  });
}

linkElements.forEach((link) => {
  link.addEventListener('click', () => {
    clearActive();
    link.classList.add('active');
  });
});