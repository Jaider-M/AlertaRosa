import { ref, readonly } from 'vue';
import type { User, RegisterData } from '../types';
import { initializeDemoUsers } from '../utils/initDemoUsers';

// Global state
const user = ref<User | null>(null);
const loading = ref<boolean>(true);

export function initAuth() {
  if (loading.value) {
    initializeDemoUsers();
    const storedUser = localStorage.getItem('currentUser');
    if (storedUser) {
      user.value = JSON.parse(storedUser);
    }
    loading.value = false;
  }
}

export function useAuth() {
  // Ensure it's initialized when used in components if not done by router yet
  initAuth();

  const login = (email: string, password: string): boolean => {
    const usersData = localStorage.getItem('users');
    const users = usersData ? JSON.parse(usersData) : [];

    const foundUser = users.find(
      (u: any) => u.email === email && u.password === password
    );

    if (foundUser) {
      const { password: _, ...userWithoutPassword } = foundUser;
      user.value = userWithoutPassword;
      localStorage.setItem('currentUser', JSON.stringify(userWithoutPassword));
      return true;
    }
    return false;
  };

  const register = (userData: RegisterData): boolean => {
    const usersData = localStorage.getItem('users');
    const users = usersData ? JSON.parse(usersData) : [];

    if (users.some((u: any) => u.email === userData.email)) {
      return false;
    }

    const newUser = {
      id: `U${Date.now()}`,
      ...userData,
      registrationDate: new Date().toISOString(),
    };

    users.push(newUser);
    localStorage.setItem('users', JSON.stringify(users));

    const { password: _, ...userWithoutPassword } = newUser;
    user.value = userWithoutPassword;
    localStorage.setItem('currentUser', JSON.stringify(userWithoutPassword));

    return true;
  };

  const logout = () => {
    user.value = null;
    localStorage.removeItem('currentUser');
  };

  return {
    user: readonly(user),
    loading: readonly(loading),
    login,
    register,
    logout,
  };
}
