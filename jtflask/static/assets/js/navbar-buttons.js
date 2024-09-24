const navbarButtonIds = [
  "charts-button",
  "tools-button",
  "basemaps-gallery-button",
];

const navbarDrawerChildrenIds = ["charts", "arcgis-tools", "basemap-gallery"];

const navbarButtonToDrawerClassMap = Object.fromEntries(
  navbarButtonIds.map((buttonId, index) => {
    return [buttonId, navbarDrawerChildrenIds[index]];
  })
);

const activeNavbarButtonClass = "navbar-button-active";
const activeNavbarDrawerClasses = ["animate__animated", "animate__slideInUp"];
const navbarDrawerClosedClass = "animate__slideOutLeft";
const navbarDrawerOpenedClass = "animate__slideInLeft";

const isMobile = () => window.innerWidth <= 768;

const isClickedButtonActive = (clickedButton) =>
  clickedButton.classList.contains(activeNavbarButtonClass);

const handleInitialState = () => {
  const chartsButton = document.querySelector(`#${navbarButtonIds[0]}`);
  chartsButton.classList.toggle(activeNavbarButtonClass);

  const defaultNavbarChild = document.querySelector(
    `#${navbarDrawerChildrenIds[0]}`
  );
  defaultNavbarChild.classList.add(...activeNavbarDrawerClasses);

  const navbarDrawer = document.querySelector("#navbar-drawer");
  navbarDrawer.classList.add("animate__animated", navbarDrawerOpenedClass);
};

const handleNavbarButtonClassUpdate = (clickedButtonId) => {
  const clickedButton = document.querySelector(`#${clickedButtonId}`);
  const otherButtons = navbarButtonIds
    .filter((buttonId) => buttonId !== clickedButtonId)
    .map((buttonId) => document.querySelector(`#${buttonId}`));

  const navbarDrawer = document.querySelector("#navbar-drawer");

  if (isMobile()) {
    if (isClickedButtonActive(clickedButton)) {
      navbarDrawer.classList.replace(
        navbarDrawerOpenedClass,
        navbarDrawerClosedClass
      );
    } else {
      navbarDrawer.classList.replace(
        navbarDrawerClosedClass,
        navbarDrawerOpenedClass
      );
    }
  }

  if (!isMobile()) {
    if (navbarDrawer.classList.contains(navbarDrawerClosedClass)) {
      navbarDrawer.classList.replace(
        navbarDrawerClosedClass,
        navbarDrawerOpenedClass
      );
    }
  }

  otherButtons.forEach((button) =>
    button.classList.remove(activeNavbarButtonClass)
  );

  clickedButton.classList.toggle(activeNavbarButtonClass);
};

const handleNavbarDrawerClassUpdate = (clickedButtonId) => {
  const activeDrawerElementId = navbarButtonToDrawerClassMap[clickedButtonId];
  const activeDrawerElement = document.querySelector(
    `#${activeDrawerElementId}`
  );

  const otherDrawerElements = navbarDrawerChildrenIds
    .filter((id) => id !== activeDrawerElementId)
    .map((drawerElementId) => document.querySelector(`#${drawerElementId}`));

  otherDrawerElements.forEach((drawerElement) =>
    drawerElement.classList.add("hidden")
  );
  activeDrawerElement.classList.remove("hidden");
  activeDrawerElement.classList.add(...activeNavbarDrawerClasses);
};

const handleCollapseButtonClick = (collapseButtonId) => {
  const navbarDrawer = document.querySelector("#navbar-drawer");
  if (navbarDrawer.classList.contains(navbarDrawerClosedClass)) {
    navbarDrawer.classList.replace(
      navbarDrawerClosedClass,
      navbarDrawerOpenedClass
    );
  } else {
    navbarDrawer.classList.replace(
      navbarDrawerOpenedClass,
      navbarDrawerClosedClass
    );
  }
};

window.dash_clientside = Object.assign({}, window.dash_clientside, {
  clientside: {
    handleNavbarButtonClick: function (...inputs) {
      //On Initial Render
      if (inputs.every((input) => input === undefined)) {
        handleInitialState();
        return;
      }
      const collapseButtonId = "collapse-button";
      const clickedButtonId = dash_clientside.callback_context.triggered_id;

      if (navbarButtonIds.includes(clickedButtonId)) {
        handleNavbarButtonClassUpdate(clickedButtonId);
        handleNavbarDrawerClassUpdate(clickedButtonId);
      }
      if (clickedButtonId === collapseButtonId) {
        handleCollapseButtonClick(collapseButtonId);
      }
    },
  },
});