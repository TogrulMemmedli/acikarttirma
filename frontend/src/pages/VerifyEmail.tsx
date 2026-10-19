
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiRequest } from "../services/api";
import "./VerifyEmail.css";

type VerifyResponse = {
  message: string;
  access_token: string;
  token_type: string;
};

export default function VerifyEmail() {
  const navigate = useNavigate();
  const [message, setMessage] = useState("E-poçt təsdiqlənir...");
  const [error, setError] = useState("");

  useEffect(() => {
    async function verifyEmail() {
      const token = new URLSearchParams(
        window.location.hash.slice(1),
      ).get("token");

      if (!token) {
        setError("Təsdiq tokeni tapılmadı. E-poçtdakı linki yenidən yoxla.");
        setMessage("");
        return;
      }

      try {
        const result = await apiRequest<VerifyResponse>(
          "/auth/verify-email",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ token }),
          },
        );

        localStorage.setItem("access_token", result.access_token);
        setMessage("E-poçt təsdiqləndi. Ana səhifəyə yönləndirilirsən...");

        navigate("/", { replace: true });
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "E-poçtu təsdiqləmək mümkün olmadı.",
        );
        setMessage("");
      }
    }

    void verifyEmail();
  }, [navigate]);

  return (
    <main className="verify-page">
      <section className="verify-card">
        <span className="verify-eyebrow">AçıqArtırma</span>
        <h1>E-poçt təsdiqi</h1>

        {message && <p role="status">{message}</p>}
        {error && <p className="verify-error" role="alert">{error}</p>}

        {error && (
          <a className="verify-link" href="/">
            Ana səhifəyə qayıt
          </a>
        )}
      </section>
    </main>
  );
}
