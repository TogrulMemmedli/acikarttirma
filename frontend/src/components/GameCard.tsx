
type GameCardProps = {
  name: string;
  description: string;
  imageUrl: string;
};

export default function GameCard({
  name,
  description,
  imageUrl,
}: GameCardProps) {
  return (
    <article className="game-card">
      <img className="game-card__image" src={imageUrl} alt={name} />
      <h3>{name}</h3>

      <p>{description}</p>

      <button type="button">Oyuna bax</button>
    </article>
  );
}
