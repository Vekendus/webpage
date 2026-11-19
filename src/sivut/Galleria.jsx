import "../App.css";
import { useEffect, useState } from "react";
import { fetchJson } from "../api.js";

function Galleria() {
  const [photos, setPhotos] = useState([]);

  useEffect(() => {
    fetchJson("/api/photos/")
      .then(setPhotos)
      .catch((error) => console.error("Portfolio-kuvien lataus epäonnistui:", error));
  }, []);

  const galleryPhotos = photos.filter((photo) => photo.show_in_gallery);

  return (
    <main className="page-shell gallery-page">
      <div className="section-lead">
        <p className="eyebrow">GALLERIA</p>
        <h2>Valokuvia, joissa on tunnetta.</h2>
      </div>

      <div className="gallery-grid">
        {galleryPhotos.map((photo) => (
          <article className="gallery-card" key={photo.id}>
            <img src={photo.image} alt={photo.title} loading="lazy" />
            <div className="gallery-card-copy">
              <p>{photo.description || "PORTFOLIO"}</p>
              <h3>{photo.title}</h3>
            </div>
          </article>
      ))}
      </div>
      {galleryPhotos.length === 0 && (
        <p>Portfolio-kuvia ei ole vielä julkaistu.</p>
      )}
    </main>
  );
}

export default Galleria;