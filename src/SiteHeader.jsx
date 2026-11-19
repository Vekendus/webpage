import { useEffect, useState } from "react";
import "./App.css";

function SiteHeader({ isHome }) {
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    if (!menuOpen) return undefined;

    function closeOnEscape(event) {
      if (event.key === "Escape") setMenuOpen(false);
    }

    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [menuOpen]);

  return (
    <header className={`site-header${isHome ? "" : " site-header-inner"}`}>
      <a
        className="wordmark"
        href={isHome ? "#alku" : "/"}
        aria-label="Hiltunen Photography, alkuun"
      >
        <span>HILTUNEN</span>
        <span className="wordmark-subtitle">PHOTOGRAPHY</span>
      </a>
      <button
        className="menu-toggle"
        type="button"
        aria-expanded={menuOpen}
        aria-controls="main-menu"
        onClick={() => setMenuOpen((open) => !open)}
      >
        {menuOpen ? "Sulje valikko" : "Valikko"}
      </button>
      <button
        className={`menu-backdrop${menuOpen ? " is-open" : ""}`}
        type="button"
        aria-label="Sulje valikko"
        tabIndex={menuOpen ? 0 : -1}
        onClick={() => setMenuOpen(false)}
      />
      <nav
        className={`main-nav${menuOpen ? " is-open" : ""}`}
        id="main-menu"
        aria-label="Päänavigointi"
        aria-hidden={!menuOpen}
      >
        <button
          className="menu-close"
          type="button"
          onClick={() => setMenuOpen(false)}
        >
          Sulje valikko <span aria-hidden="true">×</span>
        </button>
        <a href="/" onClick={() => setMenuOpen(false)}>Pääsivu</a>
        <a href="/minusta" onClick={() => setMenuOpen(false)}>Minusta</a>
        <a href="/portfolio" onClick={() => setMenuOpen(false)}>Portfolio</a>
        <a href="/palvelut" onClick={() => setMenuOpen(false)}>Palvelut</a>
        <a href="/yhteystiedot" onClick={() => setMenuOpen(false)}>Ota yhteyttä</a>
      </nav>
    </header>
  );
}

export default SiteHeader;
