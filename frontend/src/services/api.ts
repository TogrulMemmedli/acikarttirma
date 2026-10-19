const API_URL = import.meta.env.VITE_API_URL;

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      ...options.headers,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    const message =
      typeof data.detail === "string"
        ? data.detail
        : "Sorğu zamanı xəta baş verdi.";

    throw new Error(message);
  }

  return data as T;
}