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

  return (
    <main className="page-shell">
      <h1>{contactContent?.heading ?? "Yhteystiedot"}</h1>
      {contactContent?.intro && <p>{contactContent.intro}</p>}
      {contactContent?.links?.map((link) => (
        <p key={link.id}>
          <a
            className="text-link"
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