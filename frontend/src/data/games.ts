
export type Game = {
  id: number;
  name: string;
  description: string;
  imageUrl: string;
};

export const games: Game[] = [
  {
    id: 1,
    name: "Star Wars Characters",
    description:
      "Sevimli Star Wars personajlarını seç və dostunla rəqabət apar.",
    imageUrl: "https://placehold.co/600x338?text=Star+Wars",
  },
  {
    id: 2,
    name: "Anime Characters",
    description:
      "Anime personajlarından öz komandanı qur.",
    imageUrl: "https://placehold.co/600x338?text=Anime",
  },
];
