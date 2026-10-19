
import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { apiRequest } from "../services/api";
import "./Login.css";
import { useAuth } from "../context/useAuth";

type LoginResponse = {
  access_token: string;
  token_type: string;
};

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { refreshUser } = useAuth();

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.set("username", email);
      formData.set("password", password);

      const result = await apiRequest<LoginResponse>("/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      localStorage.setItem("access_token", result.access_token);
      await refreshUser();
     navigate("/", { replace: true });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Giriş zamanı xəta baş verdi.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="login-page">
      <div className="login-container">
        <header className="login-heading">
          <span className="login-eyebrow">AçıqArtırma hesabı</span>
          <h1>Yenidən xoş gəldin.</h1>
          <p>Hesabına daxil ol və oyunlara davam et.</p>
        </header>

        <section className="login-card">
          <form className="login-form" onSubmit={handleSubmit}>
            <div className="login-field">
              <label htmlFor="email">E-poçt ünvanı</label>
              <input
                id="email"
                type="email"
                placeholder="sen@example.com"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                autoComplete="email"
                required
              />
            </div>

            <div className="login-field">
              <label htmlFor="password">Şifrə</label>
              <input
                id="password"
                type="password"
                placeholder="Şifrən"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                autoComplete="current-password"
                required
              />
            </div>

            <button
              className="login-submit"
              type="submit"
              disabled={loading}
            >
              {loading ? "Daxil olunur..." : "Daxil ol"}
            </button>
          </form>

          {error && (
            <p className="login-error" role="alert">
              {error}
            </p>
          )}
        </section>

        <p className="login-footer">
          Hesabın yoxdur? <a href="/register">Qeydiyyatdan keç</a>
        </p>
      </div>
    </main>
  );
}
