"use client";
import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from "react";

interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
}

interface UserSettings {
  id: number;
  user_id: number;
  openai_api_key?: string;
  mongo_uri?: string;
  mongo_db?: string;
  mongo_collection?: string;
  embedding_model: string;
  llm_model: string;
  llm_temperature: string;
  system_prompt?: string;
  welcome_message?: string;
  theme: string;
  language: string;
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: User | null;
  settings: UserSettings | null;
  token: string | null;
  login: (email: string, password: string) => Promise<boolean>;
  register: (
    email: string,
    username: string,
    password: string,
    full_name?: string
  ) => Promise<boolean>;
  logout: () => void;
  updateSettings: (settings: Partial<UserSettings>) => Promise<boolean>;
  refreshUser: () => Promise<void>;
  isLoading: boolean;
  handleAuthError: (response: Response) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [settings, setSettings] = useState<UserSettings | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const API_BASE =
    process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

  // Cargar token desde localStorage al inicializar
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) {
      setToken(savedToken);
      verifyToken(savedToken);
    } else {
      setIsLoading(false);
    }
  }, []);

  // Verificar token y cargar usuario
  const verifyToken = async (token: string) => {
    try {
      const response = await fetch(`${API_BASE}/auth/verify-token`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        await refreshUser();
      } else {
        // Token inválido
        localStorage.removeItem("token");
        setToken(null);
        setUser(null);
        setSettings(null);
      }
    } catch (error) {
      console.error("Error verificando token:", error);
      localStorage.removeItem("token");
      setToken(null);
      setUser(null);
      setSettings(null);
    } finally {
      setIsLoading(false);
    }
  };

  // Refrescar información del usuario
  const refreshUser = async () => {
    if (!token) return;

    try {
      const response = await fetch(`${API_BASE}/auth/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        setSettings(userData.settings);
      }
    } catch (error) {
      console.error("Error cargando usuario:", error);
    }
  };

  // Función de login
  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        const newToken = data.access_token;

        setToken(newToken);
        localStorage.setItem("token", newToken);
        await refreshUser();
        return true;
      } else {
        return false;
      }
    } catch (error) {
      console.error("Error en login:", error);
      return false;
    }
  };

  // Función de registro
  const register = async (
    email: string,
    username: string,
    password: string,
    full_name?: string
  ): Promise<boolean> => {
    try {
      const response = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, username, password, full_name }),
      });

      if (response.ok) {
        // Después del registro, hacer login automático
        return await login(email, password);
      } else {
        return false;
      }
    } catch (error) {
      console.error("Error en registro:", error);
      return false;
    }
  };

  // Función de logout
  const logout = () => {
    setToken(null);
    setUser(null);
    setSettings(null);
    localStorage.removeItem("token");
  };

  // Función para actualizar configuraciones
  const updateSettings = async (
    newSettings: Partial<UserSettings>
  ): Promise<boolean> => {
    if (!token) return false;

    try {
      const response = await fetch(`${API_BASE}/settings`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newSettings),
      });

      if (response.ok) {
        const updatedSettings = await response.json();
        setSettings(updatedSettings);
        return true;
      }
      return false;
    } catch (error) {
      console.error("Error actualizando configuraciones:", error);
      return false;
    }
  };

  // Función para manejar errores de autenticación
  const handleAuthError = (response: Response) => {
    if (response.status === 401) {
      // Token expirado o inválido
      logout();
    }
  };

  const value: AuthContextType = {
    user,
    settings,
    token,
    login,
    register,
    logout,
    updateSettings,
    refreshUser,
    isLoading,
    handleAuthError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
