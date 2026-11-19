import "../App.css";
import { useEffect, useState } from "react";
import { fetchJson } from "../api.js";

function Minä(){
  const [about, setAbout] = useState(null);

  useEffect(() => {
    fetchJson("/api/about/")
      .then(setAbout)
      .catch((error) => console.error("Esittelytietojen lataus epäonnistui:", error));
  }, []);

  const paragraphs = (about?.body || "")
    .split(/\n\s*\n/)
    .filter(Boolean);
  const aboutPhotos = about?.photos ?? [];

  return(
    <main className="page-shell">
      <div className={`about-page${about?.image ? " has-image" : ""}`}>
        {about?.image && (
          <div className="about-image-wrap">
            <img src={about.image} alt={about.image_alt} />
          </div>
        )}
        <section className="about-copy">
          <p className="eyebrow">HILTUNEN PHOTOGRAPHY</p>
          <h1>{about?.heading || "Hei, ihana tutustua."}</h1>
          {paragraphs.map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
        </section>
      </div>
      {aboutPhotos.length > 0 && (
        <section className="about-photo-section">
          <div className="about-photo-heading">
            <p className="eyebrow">HILTUNEN PHOTOGRAPHY</p>
            <h2>Kuvia minusta</h2>
          </div>
          <div className="about-photo-gallery">
            {aboutPhotos.map((photo) => (
              <figure className="about-photo-card" key={photo.id}>
                <img src={photo.image} alt={photo.alt} loading="lazy" />
                {photo.caption && <figcaption>{photo.caption}</figcaption>}
              </figure>
            ))}
          </div>
        </section>
      )}
    </main>
  )
};

export default Minä;