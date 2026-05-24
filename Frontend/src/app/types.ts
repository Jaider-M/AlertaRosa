export type UserRole = 'patient' | 'doctor' | 'manager';

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  phone?: string;
  specialization?: string;
  registrationDate: string;
}

export interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => boolean;
  register: (userData: RegisterData) => boolean;
  logout: () => void;
}

export interface RegisterData {
  email: string;
  password: string;
  name: string;
  role: UserRole;
  phone?: string;
  specialization?: string;
  registro_medico?: string;
}
