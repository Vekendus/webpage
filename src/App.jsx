import Etusivu from "./sivut/Etusivu.jsx";
import Galleria from "./sivut/Galleria.jsx";
import Palvelut from "./sivut/Palvelut.jsx";
import Yhteystiedot from "./sivut/Yhteystiedot.jsx";
import Minä from "./sivut/Minä.jsx";
import SiteHeader from "./SiteHeader.jsx";

function App() {
  const path = decodeURIComponent(window.location.pathname)
    .replace(/\/+$/, "")
    .toLowerCase() || "/";
  let page = <Etusivu />;
  if (path === "/portfolio") page = <Galleria />;
  if (path === "/palvelut") page = <Palvelut />;
  if (path === "/yhteystiedot") page = <Yhteystiedot />;
  if (path === "/minä" || path === "/minusta") page = <Minä />;

  return (
    <>
      <SiteHeader isHome={path === "/"} />
      {page}
    </>
  );
}

export default App;
