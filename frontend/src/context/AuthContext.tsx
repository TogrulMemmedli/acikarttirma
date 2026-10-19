
import {
  useCallback,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { apiRequest } from "../services/api";
import type { CurrentUser } from "./current-user";
import { AuthContext } from "./auth-context";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = useCallback(async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }

    setLoading(true);

    try {
      const currentUser = await apiRequest<CurrentUser>("/auth/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setUser(currentUser);
    } catch (error) {
        localStorage.removeItem("access_token");
        setUser(null);
        throw error;
        } finally {
        setLoading(false);
    }
  }, []);

  useEffect(() => {
    let active = true;

    async function initializeAuth() {
        const token = localStorage.getItem("access_token");

        if (!token) {
        if (active) {
            setUser(null);
            setLoading(false);
        }
        return;
        }

        try {
        const currentUser = await apiRequest<CurrentUser>("/auth/me", {
            headers: {
            Authorization: `Bearer ${token}`,
            },
        });

        if (active) {
            setUser(currentUser);
        }
        } catch {
        localStorage.removeItem("access_token");

        if (active) {
            setUser(null);
        }
        } finally {
        if (active) {
            setLoading(false);
        }
        }
    }

    void initializeAuth();

    return () => {
        active = false;
    };
    }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("access_token");
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, loading, refreshUser, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}