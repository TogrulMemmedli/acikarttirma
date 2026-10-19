
import { createContext } from "react";
import type { CurrentUser } from "./current-user";

export type AuthContextType = {
  user: CurrentUser | null;
  loading: boolean;
  refreshUser: () => Promise<void>;
  logout: () => void;
};

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined,
);
