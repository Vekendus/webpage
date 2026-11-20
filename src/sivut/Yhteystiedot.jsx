import "../App.css";
import { useEffect, useState } from "react";
import { fetchJson } from "../api.js";

function Yhteystiedot() {
  const [pageContent, setPageContent] = useState(null);

  useEffect(() => {
    fetchJson("/api/pages/")
      .then(setPageContent)
      .catch((error) => console.error("Sivutekstien lataus epäonnistui:", error));
  }, []);

  const contactContent = pageContent?.contact;
  const links = contactContent?.links ?? [];
  const reservationContact = links.find(
    (link) => link.destination_type === "whatsapp",
  );
  const instagramLink = links.find(
    (link) => link.label.toLowerCase() === "instagram",
  );
  const otherLinks = links.filter(
    (link) => link !== reservationContact && link !== instagramLink,
  );
  const phoneHref = reservationContact?.phone_number?.replace(/[^\d+]/g, "");

  return (
    <main className="page-shell contact-page">
      <h1>{contactContent?.heading ?? "Yhteystiedot"}</h1>
      {contactContent?.intro && <p>{contactContent.intro}</p>}
      {reservationContact?.phone_number && (
        <div className="contact-reservations">
          <p className="contact-reservations-label">
            Ajanvaraukset puhelimitse
          </p>
          <a
            className="contact-phone-link"
            href={`tel:${phoneHref}`}
          >
            {reservationContact.phone_number}
          </a>
        </div>
      )}
      {instagramLink && (
        <a
          className="contact-instagram-link"
          href={instagramLink.url}
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Instagram"
          title="Instagram"
        >
          <svg
            aria-hidden="true"
            viewBox="0 0 48 48"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <defs>
              <linearGradient
                id="instagram-gradient"
                x1="8"
                y1="40"
                x2="40"
                y2="8"
                gradientUnits="userSpaceOnUse"
              >
                <stop stopColor="#FFC107" />
                <stop offset=".5" stopColor="#F44336" />
                <stop offset="1" stopColor="#9C27B0" />
              </linearGradient>
            </defs>
            <rect
              x="5"
              y="5"
              width="38"
              height="38"
              rx="11"
              stroke="url(#instagram-gradient)"
              strokeWidth="3"
            />
            <circle
              cx="24"
              cy="24"
              r="9"
              stroke="url(#instagram-gradient)"
              strokeWidth="3"
            />
            <circle cx="36" cy="12" r="2.25" fill="#F44336" />
          </svg>
        </a>
      )}
      {otherLinks.map((link) => (
        <p key={link.id}>
          <a
            className="contact-link"
            href={link.url}
            target="_blank"
            rel="noopener noreferrer"
          >
            {link.label}
          </a>
        </p>
      ))}
    </main>
  );
}

export default Yhteystiedot;