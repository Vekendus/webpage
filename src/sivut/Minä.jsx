import "../App.css";
import { useEffect, useState } from "react";
import { fetchJson } from "../api.js";

function Minä(){
  const [about, setAbout] = useState(null);
  const [pageContent, setPageContent] = useState(null);

  useEffect(() => {
    fetchJson("/api/about/")
      .then(setAbout)
      .catch((error) => console.error("Esittelytietojen lataus epäonnistui:", error));
    fetchJson("/api/pages/")
      .then(setPageContent)
      .catch((error) => console.error("Sivutekstien lataus epäonnistui:", error));
  }, []);

  const paragraphs = (about?.body || "")
    .split(/\n\s*\n/)
    .filter(Boolean);
  const aboutPhotos = about?.photos ?? [];
  const hasImages = Boolean(about?.image) || aboutPhotos.length > 0;

  return(
    <main className="page-shell">
      <div className={`about-page${hasImages ? " has-images" : ""}`}>
        <section className="about-copy">
          <p className="eyebrow">
            {pageContent?.about?.eyebrow ?? "HILTUNEN PHOTOGRAPHY"}
          </p>
          <h1>{about?.heading || "Hei, ihana tutustua."}</h1>
          {paragraphs.map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
        </section>
        <div className="about-page-images">
          {about?.image && (
            <div className="about-image-wrap">
              <img src={about.image} alt={about.image_alt} />
            </div>
          )}
          {aboutPhotos.length > 0 && (
            <section className="about-photo-section">
              <div className="about-photo-heading">
                <p className="eyebrow">
                  {pageContent?.about?.photos_eyebrow ?? "HILTUNEN PHOTOGRAPHY"}
                </p>
                <h2>{pageContent?.about?.photos_heading ?? "Kuvia minusta"}</h2>
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
        </div>
      </div>
    </main>
  )
};

export default Minä;