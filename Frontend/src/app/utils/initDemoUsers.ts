export function initializeDemoUsers() {
  const existingUsers = localStorage.getItem('users');

  if (!existingUsers) {
    const demoUsers = [
      {
        id: 'M001',
        email: 'gerente@alertarosa.com',
        password: 'admin123',
        name: 'Dr. Roberto Sánchez',
        role: 'manager',
        phone: '+34 600 111 222',
        registrationDate: '2025-01-15T10:00:00Z',
      },
      {
        id: 'D001',
        email: 'doctor@alertarosa.com',
        password: 'doctor123',
        name: 'Dra. María González',
        role: 'doctor',
        phone: '+34 600 222 333',
        specialization: 'Oncología Mamaria',
        registrationDate: '2025-02-01T10:00:00Z',
      },
      {
        id: 'P001',
        email: 'paciente@alertarosa.com',
        password: 'paciente123',
        name: 'Ana Martínez Ruiz',
        role: 'patient',
        phone: '+34 600 333 444',
        registrationDate: '2025-03-10T10:00:00Z',
      },
    ];

    localStorage.setItem('users', JSON.stringify(demoUsers));
  }
}
