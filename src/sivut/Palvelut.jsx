import "../App.css";
import { useEffect, useState } from "react";
import { fetchJson } from "../api.js";

function Palvelut() {
  const [services, setServices] = useState([]);
  const [pageContent, setPageContent] = useState(null);

  useEffect(() => {
    fetchJson("/api/services/")
      .then(setServices)
      .catch((error) => console.error("Palveluiden lataus epäonnistui:", error));
    fetchJson("/api/pages/")
      .then(setPageContent)
      .catch((error) => console.error("Sivutekstien lataus epäonnistui:", error));
  }, []);

  const servicesContent = pageContent?.services;

  return (
    <main className="page-shell">
      <h1>{servicesContent?.heading ?? "Palvelut"}</h1>
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
        <p>
          {servicesContent?.empty_message ??
            "Palveluiden tietoja ei ole vielä lisätty."}
        </p>
      )}
    </main>
  );
}

export default Palvelut;