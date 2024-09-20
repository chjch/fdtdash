export const hideSplashScreen = () => {
  const [jaxLogoH1, twinLogoH1] = document.querySelectorAll(".logo h1");
  const logoImage = document.querySelector(".logo-image")
  const splashDiv = document.querySelector(".splash");

  jaxLogoH1.classList.add("animate__fadeOutUp");
  twinLogoH1.classList.replace('animate__delay-1s', 'animate__fadeOutDown')

  twinLogoH1.addEventListener('animationend', () => {
    logoImage.removeAttribute('hidden')
    // logoImage.classList.add('animate__animated', 'animate__fadeIn')
  });

  logoImage.addEventListener('animationend', () => {
    logoImage.classList.add('animate__fadeOut')
    splashDiv.classList.add("animate__animated", "animate__fadeOutUp");
  });

  splashDiv.addEventListener('animationend', () => {
      splashDiv.setAttribute('hidden', 'true')
  });
} 