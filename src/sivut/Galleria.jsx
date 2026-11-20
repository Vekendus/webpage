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

  const chapterMatch = window.location.pathname.match(/^\/portfolio\/(\d+)\/?$/);
  const selectedChapterId = chapterMatch ? Number(chapterMatch[1]) : null;
  const selectedChapter = chapters.find(
    (chapter) => chapter.id === selectedChapterId,
  );
  const galleryContent = pageContent?.gallery;
  const emptyMessage =
    galleryContent?.empty_message ?? "Portfolio-kuvia ei ole vielä julkaistu.";

  return (
    <main className="page-shell gallery-page">
      <div className="section-lead">
        <p className="eyebrow">{galleryContent?.eyebrow ?? "GALLERIA"}</p>
        <h2>{galleryContent?.heading ?? "Valokuvia, joissa on tunnetta."}</h2>
      </div>

      {selectedChapterId !== null ? (
        <section className="gallery-chapter">
          <a className="gallery-back-link" href="/portfolio">
            ← Takaisin portfolioon
          </a>
          {selectedChapter ? (
            <>
              <div className="gallery-chapter-heading">
                <h3>{selectedChapter.title}</h3>
                {selectedChapter.description && (
                  <p>{selectedChapter.description}</p>
                )}
              </div>
              {selectedChapter.photos.length > 0 ? (
                <div className="gallery-grid">
                  {selectedChapter.photos.map((photo) => (
                    <article className="gallery-card" key={photo.id}>
                      <img src={photo.image} alt={photo.title} loading="lazy" />
                      <div className="gallery-card-copy">
                        <p>{photo.description || "PORTFOLIO"}</p>
                        <h3>{photo.title}</h3>
                      </div>
                    </article>
                  ))}
                </div>
              ) : (
                <p>{emptyMessage}</p>
              )}
            </>
          ) : (
            <p>Tätä portfoliokategoriaa ei löytynyt.</p>
          )}
        </section>
      ) : chapters.length > 0 ? (
        <div className="portfolio-chapter-grid">
          {chapters.map((chapter) => (
            <a
              className="portfolio-chapter-card"
              href={`/portfolio/${chapter.id}`}
              key={chapter.id}
            >
              <div
                className={`portfolio-chapter-cover${chapter.title === "Valmistujaiset" ? " portfolio-chapter-cover-inset" : ""}`}
              >
                {chapter.cover_image ? (
                  <img
                    src={chapter.cover_image}
                    alt=""
                    loading="lazy"
                  />
                ) : (
                  <span className="portfolio-chapter-cover-empty">
                    HILTUNEN PHOTOGRAPHY
                  </span>
                )}
              </div>
              <div className="portfolio-chapter-copy">
                <h3>{chapter.title}</h3>
                {chapter.description && <p>{chapter.description}</p>}
              </div>
            </a>
          ))}
        </div>
      ) : (
        <p>{emptyMessage}</p>
      )}
    </main>
  );
}

export default Galleria;
