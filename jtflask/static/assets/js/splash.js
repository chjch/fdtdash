const JTSplashPage = (() => {
  "use strict";

  const hideSplash = () => {
    const [jaxLogoH1, twinLogoH1] = document.querySelectorAll(".logo h1");
    const logoImage = document.querySelector(".logo-image");
    const splashDiv = document.querySelector(".splash");

    twinLogoH1.addEventListener("animationend", () => {
      logoImage.style.visibility = "visible";
      logoImage.classList.add(
        "animate__animated",
        "animate__slow",
        "animate__fadeIn"
      );
    });

    logoImage.addEventListener("animationend", () => {
      jaxLogoH1.classList.remove("animate__delay-1s", "animate__fadeIn");
      twinLogoH1.classList.remove("animate__delay-3s", "animate__fadeIn");
      //jaxLogoH1.classList.add("animate__heartBeat");
      twinLogoH1.classList.add("animate__bounce", "animate_faster");
      splashDiv.classList.add(
        "animate__animated",
        "animate__slow",
        "animate__fadeOut",
        "animate__delay-1s"
      );
      setTimeout(() => {
        splashDiv.setAttribute("hidden", "true");
      }, 3000);
    });

    splashDiv.addEventListener("click", () => {
      splashDiv.setAttribute("hidden", "true");
    });
  };
  // Return the public API
  return {
    hideSplash: hideSplash,
  };
})();
