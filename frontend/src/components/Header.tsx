
import { Link } from "react-router-dom";
import { useAuth } from "../context/useAuth";

export default function Header() {
  const { user, loading, logout } = useAuth();

  return (
    <header className="site-header">
      <div className="header-inner">
        <Link
          className="brand"
          to="/"
          aria-label="AçıqArtırma ana səhifə"
        >
          <span className="brand-mark">A</span>
          <span>AçıqArtırma</span>
        </Link>

        <nav className="header-nav" aria-label="Əsas naviqasiya">
          {!loading &&
            (user ? (
              <>
                <span className="header-username">
                  {user.username}
                </span>
                <button
                  className="logout-button"
                  type="button"
                  onClick={logout}
                >
                  Çıxış
                </button>
              </>
            ) : (
              <>
                <Link className="login-link" to="/login">
                  Login
                </Link>
                <Link className="register-link" to="/register">
                  Register
                </Link>
              </>
            ))}
        </nav>
      </div>
    </header>
  );
}
