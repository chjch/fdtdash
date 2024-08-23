export const hideSplashScreen = () => {
  const [jaxLogoH1, twinLogoH1] = document.querySelectorAll(".logo h1");
  jaxLogoH1.classList.add("animate__fadeOutUp");
  twinLogoH1.classList.replace('animate__delay-1s', 'animate__fadeOutDown')
  twinLogoH1.classList.add("animate__fadeOutDown");
  setTimeout(() => {
    const splashDiv = document.querySelector(".splash");
    splashDiv.classList.add("animate__animated", "animate__fadeOut");
    splashDiv.setAttribute('hidden', 'true')
  }, 2000);
}