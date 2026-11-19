import "../App.css";
import { useEffect, useState } from "react";
import { fetchJson } from "../api.js";

function Palvelut() {
  const [services, setServices] = useState([]);

  useEffect(() => {
    fetchJson("/api/services/")
      .then(setServices)
      .catch((error) => console.error("Palveluiden lataus epäonnistui:", error));
  }, []);

  return (
    <main className="page-shell">
      <h1>Palvelut</h1>
      <div className="service-list">
        {services.map((service) => (
          <div className="service-page-item" key={service.id}>
            <div>
              <h2 className="service-title">{service.title}</h2>
              {service.description && (
                <p className="service-detail">{service.description}</p>
              )}
            </div>
            <p className="service-price">{service.price}</p>
          </div>
        ))}
      </div>
      {services.length === 0 && (
        <p>Palveluiden tietoja ei ole vielä lisätty.</p>
      )}
    </main>
  );
}

export default Palvelut;