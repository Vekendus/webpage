import "../App.css";
import { useEffect, useState } from "react";
import { fetchJson } from "../api.js";

function ArrowIcon() {
  return <span aria-hidden="true">↗</span>;
}

function App() {
  const [activeHeroSlide, setActiveHeroSlide] = useState(0);
  const [previousHeroSlide, setPreviousHeroSlide] = useState(null);
  const [slideshowPhotos, setSlideshowPhotos] = useState([]);
  const [about, setAbout] = useState(null);
  const [services, setServices] = useState([]);

  useEffect(() => {
    fetchJson("/api/slideshow/")
      .then(setSlideshowPhotos)
      .catch((error) => console.error("Diaesityskuvien lataus epäonnistui:", error));
    fetchJson("/api/about/")
      .then(setAbout)
      .catch((error) => console.error("Esittelytietojen lataus epäonnistui:", error));
    fetchJson("/api/services/")
      .then(setServices)
      .catch((error) => console.error("Palveluiden lataus epäonnistui:", error));
  }, []);

  const heroPhotos = slideshowPhotos;
  useEffect(() => {
    if (heroPhotos.length < 2) return;

    const timer = setInterval(() => {
      setPreviousHeroSlide(activeHeroSlide);
      setActiveHeroSlide((current) => (current + 1) % heroPhotos.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [activeHeroSlide, heroPhotos.length]);
  return (
    <>
      <main>
        <section className="hero" id="alku">
          {previousHeroSlide !== null && (
            <img
              className={`hero-image hero-image-slide-${previousHeroSlide + 1} hero-image-leaving`}
              src={heroPhotos[previousHeroSlide]?.image}
              alt=""
              aria-hidden="true"
              key={`leaving-${previousHeroSlide}`}
            />
          )}
          <img
            className={`hero-image hero-image-slide-${activeHeroSlide + 1}${previousHeroSlide !== null ? " hero-image-entering" : ""}`}
            src={
              heroPhotos[activeHeroSlide]?.image ??
                "https://drive.google.com/thumbnail?id=1inyRz6tVAllbTsorqybvIaD7voqZg8S3&sz=w1200"
            }
            alt=""
            key={`active-${activeHeroSlide}`}
          />
          <div className="hero-shade" />
          <div className="hero-content">
            <p className="eyebrow">Pieniä hetkiä, suuria tarinoita</p>
            <h1>
              Tehdään
              <br />
              onnellisuudesta <em> ikuista.</em>
            </h1>
            <p className="hero-copy">
              Rakkauden täyteisiä hetkiä ja pieniä yksityiskohtia - tarinoita joihin on ihana palata.
            </p>
          </div>
          <p className="hero-caption">VALOA, LÄHEISYYTTÄ JA ELÄMÄÄ</p>
          <a className="scroll-cue" href="#galleria" aria-label="Vieritä galleriaan">
            <span />
          </a>
        </section>

        <section className="intro section-wrap">
          <p className="eyebrow">HILTUNEN PHOTOGRAPHY</p>
          <img
            className="intro-photo"
            src="/images/home-intro.jpg"
            alt="Pari tanssii luonnonvalossa metsäaukealla."
            loading="lazy"
          />
          <div className="intro-content">
            <h2>
              Kauneimmat kuvat syntyvät vähiten suunnitelluissa hetkissä
            </h2>
            <p className="intro-copy">
              Valokuvia joissa näkyy aitous, persoonallisuus ja ennen kaikkea rakkaus.
            </p>
          </div>
        </section>

        <section className="gallery section-wrap" id="galleria">
          <div className="section-heading" />
          <div className="story-grid" />
        </section>

        <section className="about" id="about">
          <div className="about-image-wrap">
            <img
              src={
                about?.image ??
                "https://drive.google.com/thumbnail?id=1_5Z4WvbisPIyBE6Glp63ln-NwABmfxA7&sz=w1200"
              }
              alt={about?.image_alt || "Valokuvaaja luonnonvalossa"}
              loading="lazy"
            />
            <span className="image-stamp">LUONNOLLISESTI SINUN</span>
          </div>
          <div className="about-copy">
            <p className="eyebrow">KUKA KAMERAN TAKANA?</p>
            <h2>{about?.heading || "Hei, ihana tutustua."}</h2>
            <p>
              {about?.short_text ||
                "Minulle tärkeintä on, että tunnet olosi nähdyksi — ja saat kuvia, joissa tunnistat itsesi."}
            </p>
            <a className="about-more-link" href="/minusta">
              Lisää minusta <ArrowIcon />
            </a>
          </div>
        </section>

        <section className="services section-wrap" id="palvelut">
          <div className="section-heading">
            <div>
              <p className="eyebrow">KUVAUSPALVELUT</p>
              <h2>Sinun tärkeät hetkesi</h2>
            </div>
          </div>
          <div className="service-list">
            {services.slice(0, 3).map((service) => (
              <a href="#yhteys" key={service.id}>
                <span className="service-title">{service.title}</span>
                <span className="service-detail">{service.description}</span>
                <span className="service-price">{service.price}</span>
                <ArrowIcon />
              </a>
            ))}
          </div>
        </section>

        <section className="contact" id="yhteys">
          <p className="eyebrow">ALOITETAANKO JOTAIN IHANAA?</p>
          <h2>
            Sinun tarinasi
            <br />
            <em>ansaitsee tulla nähdyksi.</em>
          </h2>

          <a className="button button-dark" href="/yhteystiedot">
            Ota yhteyttä <ArrowIcon />
          </a>
        </section>
      </main>

      <footer className="site-footer">
        <a className="wordmark footer-wordmark" href="#alku">
          <span>HILTUNEN</span>
          <span className="wordmark-subtitle">PHOTOGRAPHY</span>
        </a>
        <a className="footer-back-to-top" href="#alku">
          Takaisin alkuun ↑
        </a>
        <span className="copyright">
          © {new Date().getFullYear()} Hiltunen Photography
        </span>
      </footer>
    </>
  );
}

export default App;
