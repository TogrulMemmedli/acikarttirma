
import { useState, type FormEvent } from "react";
import { apiRequest } from "../services/api";
import "./Register.css";

type RegisterResponse = {
  id: number;
  username: string;
  email: string;
  is_verified: boolean;
  message: string;
};

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setMessage("");
    setError("");
    setLoading(true);

    try {
      const result = await apiRequest<RegisterResponse>(
        "/auth/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username,
            email,
            password,
          }),
        },
      );

      setMessage(result.message);
      setUsername("");
      setEmail("");
      setPassword("");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Qeydiyyat zamanı xəta baş verdi.",
      );
    } finally {
      setLoading(false);
    }
  }

return (
  <main className="register-page">
    <div className="register-container">
      <header className="register-heading">
        <span className="register-eyebrow">AçıqArtırma hesabı</span>
        <h1>Bizə qoşul.</h1>
        <p>
          Hesabını yarat, oyun formatlarını kəşf et və
          dostlarınla rəqabətə başla.
        </p>
      </header>

      <section className="register-card">
        <form className="register-form" onSubmit={handleSubmit}>
          <div className="register-field">
            <label htmlFor="username">İstifadəçi adı</label>
            <input
              id="username"
              type="text"
              placeholder="Məsələn, oyunçu123"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              minLength={3}
              maxLength={30}
              autoComplete="username"
              required
            />
          </div>

          <div className="register-field">
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

          <div className="register-field">
            <label htmlFor="password">Şifrə</label>
            <input
              id="password"
              type="password"
              placeholder="Ən azı 8 simvol"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              minLength={8}
              autoComplete="new-password"
              required
            />
          </div>

          <button
            className="register-submit"
            type="submit"
            disabled={loading}
          >
            {loading ? "Qeydiyyat edilir..." : "Hesab yarat"}
            {!loading && <span aria-hidden="true">↗</span>}
          </button>
        </form>

        {message && <p className="register-message" role="status">{message}</p>}
        {error && <p className="register-error" role="alert">{error}</p>}
      </section>

      <p className="register-footer">
        Artıq hesabın var? <a href="/login">Daxil ol</a>
      </p>
    </div>
  </main>
);

}
