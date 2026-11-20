import "../App.css";
import { useEffect, useState } from "react";
import { fetchJson } from "../api.js";

function Galleria() {
  const [chapters, setChapters] = useState([]);
  const [pageContent, setPageContent] = useState(null);

  useEffect(() => {
    fetchJson("/api/portfolio/")
      .then(setChapters)
      .catch((error) => console.error("Portfolio-kuvien lataus epäonnistui:", error));
    fetchJson("/api/pages/")
      .then(setPageContent)
      .catch((error) => console.error("Sivutekstien lataus epäonnistui:", error));
  }, []);

  const hasPhotos = chapters.some((chapter) => chapter.photos.length > 0);
  const galleryContent = pageContent?.gallery;

  return (
    <main className="page-shell gallery-page">
      <div className="section-lead">
        <p className="eyebrow">{galleryContent?.eyebrow ?? "GALLERIA"}</p>
        <h2>
          {galleryContent?.heading ?? "Valokuvia, joissa on tunnetta."}
        </h2>
      </div>

      {chapters
        .filter((chapter) => chapter.photos.length > 0)
        .map((chapter) => (
        <section className="gallery-chapter" key={chapter.id}>
          <div className="gallery-chapter-heading">
            <h3>{chapter.title}</h3>
            {chapter.description && <p>{chapter.description}</p>}
          </div>
          {chapter.photos.length > 0 && (
            <div className="gallery-grid">
              {chapter.photos.map((photo) => (
                <article className="gallery-card" key={photo.id}>
                  <img src={photo.image} alt={photo.title} loading="lazy" />
                  <div className="gallery-card-copy">
                    <p>{photo.description || "PORTFOLIO"}</p>
                    <h3>{photo.title}</h3>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      ))}
      {!hasPhotos && (
        <p>
          {galleryContent?.empty_message ??
            "Portfolio-kuvia ei ole vielä julkaistu."}
        </p>
      )}
    </main>
  );
}

export default Galleria;