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
        aria-label={menuOpen ? "Sulje valikko" : "Avaa valikko"}
        aria-expanded={menuOpen}
        aria-controls="main-menu"
        onClick={() => setMenuOpen((open) => !open)}
      >
        <svg className="menu-icon" viewBox="0 0 24 24" aria-hidden="true">
          <g className="menu-lines">
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </g>
          <g className="menu-cross">
            <line x1="6" y1="6" x2="18" y2="18" />
            <line x1="18" y1="6" x2="6" y2="18" />
          </g>
        </svg>
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
        <a href="/" onClick={() => setMenuOpen(false)}>Pääsivu</a>
        <a href="/minusta" onClick={() => setMenuOpen(false)}>Minusta</a>
        <a href="/portfolio" onClick={() => setMenuOpen(false)}>Portfolio</a>
        <a href="/palvelut" onClick={() => setMenuOpen(false)}>Palvelut</a>
        <a href="/yhteystiedot" onClick={() => setMenuOpen(false)}>Ota yhteyttä</a>
        {import.meta.env.MODE !== "demo" && (
          <a
            className="nav-admin-link"
            href="/admin/"
            onClick={() => setMenuOpen(false)}
          >
            Ylläpito
          </a>
        )}
      </nav>
    </header>
  );
}

export default SiteHeader;
