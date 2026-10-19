
import GameCard from "./components/GameCard";
import { games } from "./data/games";
import "./App.css";

function App() {
  return (
    <div className="app-shell">

      <main className="home-page">
        <section className="hero">
          <div className="hero-content">
            <span className="eyebrow">
              <span className="status-dot" />
              DOSTLARINLA OYNA
            </span>

            <h1>
              Oyunu sən seç.
              <br />
              <span>Qələbəni sən qazan.</span>
            </h1>

            <p className="hero-description">
              Öz komandanı qur, büdcəni ağıllı idarə et və
              dostlarınla unudulmaz hərrac rəqabətinə qoşul.
            </p>

            <a className="hero-button" href="#games">
              Oyunları kəşf et
              <span aria-hidden="true">↗</span>
            </a>

            <div className="hero-note">
              <span className="hero-note-icon">✦</span>
              Qeydiyyatsız oyun sessiyaları
            </div>
          </div>

          <div className="hero-visual" aria-hidden="true">
            <div className="orbit orbit-one" />
            <div className="orbit orbit-two" />

            <div className="hero-symbol">
              <span>AA</span>
              <div className="symbol-line" />
              <small>BUILD YOUR TEAM</small>
            </div>

            <div className="floating-card floating-card-top">
              <span className="mini-icon">✦</span>
              <div>
                <strong>Strategiya</strong>
                <small>Hər seçim önəmlidir</small>
              </div>
            </div>

            <div className="floating-card floating-card-bottom">
              <span className="mini-icon">⚡</span>
              <div>
                <strong>Rəqabətə hazırsan?</strong>
                <small>Oyuna qoşul</small>
              </div>
            </div>
          </div>
        </section>

        <section className="games-section" id="games">
          <div className="section-heading">
            <div>
              <span className="section-kicker">KATALOQ</span>
              <h2>Oyunları kəşf et</h2>
              <p>Sənə uyğun oyunu seç və rəqabətə başla.</p>
            </div>

            <span className="game-count">
              {games.length} oyun
            </span>
          </div>

          <div className="games-grid">
            {games.map((game) => (
              <GameCard
                key={game.id}
                name={game.name}
                description={game.description}
                imageUrl={game.imageUrl}
              />
            ))}
          </div>
        </section>

        <footer className="site-footer">
          <span>AçıqArtırma</span>
          <p>Strategiya. Rəqabət. Komanda.</p>
        </footer>
      </main>
    </div>
  );
}

export default App;
