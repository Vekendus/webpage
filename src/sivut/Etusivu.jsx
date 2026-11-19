import "../App.css";
import { useEffect, useState } from "react";
import { fetchJson } from "../api.js";

function ArrowIcon() {
  return <span aria-hidden="true">↗</span>;
}

function App() {
  const [activeHeroSlide, setActiveHeroSlide] = useState(0);
  const [previousHeroSlide, setPreviousHeroSlide] = useState(null);
  const [photos, setPhotos] = useState([]);
  const [about, setAbout] = useState(null);
  const [services, setServices] = useState([]);

  useEffect(() => {
    fetchJson("/api/photos/")
      .then(setPhotos)
      .catch((error) => console.error("Kuvien lataus epäonnistui:", error));
    fetchJson("/api/about/")
      .then(setAbout)
      .catch((error) => console.error("Esittelytietojen lataus epäonnistui:", error));
    fetchJson("/api/services/")
      .then(setServices)
      .catch((error) => console.error("Palveluiden lataus epäonnistui:", error));
  }, []);

  const heroPhotos = photos.filter((photo) =>
    ["01", "02", "03", "04"].includes(photo.slot_code)
  );
  const galleryPhotos = photos.filter((photo) => photo.show_in_gallery);
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
              className="hero-image hero-image-leaving"
              src={heroPhotos[previousHeroSlide]?.image}
              alt=""
              aria-hidden="true"
              key={`leaving-${previousHeroSlide}`}
            />
          )}
          <img
            className={`hero-image${previousHeroSlide !== null ? " hero-image-entering" : ""}`}
            src={
              heroPhotos[activeHeroSlide]?.image ??
                "https://drive.google.com/thumbnail?id=1inyRz6tVAllbTsorqybvIaD7voqZg8S3&sz=w1200"
            }
            alt=""
            key={`active-${activeHeroSlide}`}
          />
          <div className="hero-shade" />
          <div className="hero-content">
            <p className="eyebrow">Oman näköistä kuvaamista · SUOMI</p>
            <h1>
              Tehdään
              <br />
              onnellisuudesta <em> ikuista.</em>
            </h1>
            <p className="hero-copy">
              Aitoja kohtaamisia ja pieniä yksityiskohtia — tarinoita, joihin on
              ihana palata.
            </p>
          </div>
          <p className="hero-caption">VALOA, LÄHEISYYTTÄ JA ELÄMÄÄ</p>
          <a className="scroll-cue" href="#galleria" aria-label="Vieritä galleriaan">
            <span />
          </a>
        </section>

        <section className="intro section-wrap">
          <p className="eyebrow">HILTUNEN PHOTOGRAPHY</p>
          <h2>
            Kauneimmat kuvat eivät pyydä poseeraamaan.
            <span> Ne antavat olla oma itsesi.</span>
          </h2>
          <p className="intro-copy">
            Minun kanssani sinun ei tarvitse osata olla kameran edessä —
            riittää, että tulet paikalle.
          </p>
        </section>

        <section className="gallery section-wrap" id="galleria">
          <div className="section-heading">
          </div>
          <div className="story-grid">
            {galleryPhotos.map((photo, index) => (
              <article
                className={`story-card story-card-${index + 1}`}
                key={photo.id}
              >
                <img src={photo.image} alt={photo.title} loading="lazy" />
                <p className="eyebrow">{photo.description || "PORTFOLIO"}</p>
                <div className="story-caption">
                  <h3>{photo.title}</h3>
                </div>
              </article>
            ))}
          </div>
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
            <a className="text-link" href="#yhteys">
              Kerro tarinasi <ArrowIcon />
            </a>
          </div>
        </section>

        <section className="services section-wrap" id="palvelut">
          <div className="section-heading">
            <div>
              <p className="eyebrow">KUVAUSPALVELUT</p>
              <h2>Sinun tärkeät hetkesi</h2>
            </div>
            <p className="section-note">Kuvaus suunnitellaan aina yhdessä.</p>
          </div>
          <div className="service-list">
            {services.slice(0, 3).map((service, index) => (
              <a href="#yhteys" key={service.id}>
                <span className="service-number">
                  {String(index + 1).padStart(2, "0")}
                </span>
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

          <a className="button button-dark" href="mailto:">
            Ota yhteyttä <ArrowIcon />
          </a>
        </section>
      </main>

      <footer className="site-footer">
        <a className="wordmark footer-wordmark" href="#alku">
          <span>HILTUNEN</span>
          <span className="wordmark-subtitle">PHOTOGRAPHY</span>
        </a>
        <p>Valokuvia, jotka tuntuvat.</p>
        <a href="#alku">Takaisin alkuun ↑</a>
        <span className="copyright">
          © {new Date().getFullYear()} Hiltunen Photography
        </span>
      </footer>
    </>
  );
}

export default App;
