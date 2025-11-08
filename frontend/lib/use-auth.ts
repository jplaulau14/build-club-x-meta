import { useState } from "react";
import { login as apiLogin, register as apiRegister, LoginResponse } from "./api";

export function useAuth() {
  const [session, setSession] = useState<LoginResponse | null>(() => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("session");
      return stored ? JSON.parse(stored) : null;
    }
    return null;
  });
  const [isLoading, setIsLoading] = useState(false);

  const login = async (username: string, password: string) => {
    const response = await apiLogin(username, password);
    setSession(response);
    if (typeof window !== "undefined") {
      localStorage.setItem("session", JSON.stringify(response));
    }
    return response;
  };

  const register = async (username: string, password: string) => {
    await apiRegister(username, password);
    return login(username, password);
  };

  const logout = () => {
    setSession(null);
    if (typeof window !== "undefined") {
      localStorage.removeItem("session");
    }
  };

  return { session, isLoading, login, register, logout };
}
