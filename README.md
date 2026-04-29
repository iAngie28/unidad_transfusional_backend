unidad-transfusional/
├── backend/
│   ├── manage.py
│   ├── config/                 # Configuración central (settings, urls, wsgi)
│   ├── apps/                   # Aplicaciones de negocio (módulos)
│   │   ├── users/              # Gestión de Bioquímicos y Jefes
│   │   ├── pacientes/          # M1 y M2 (Pacientes y Grupo Sanguíneo)
│   │   ├── hemocomponentes/    # M3 (Stock y Trazabilidad)
│   │   ├── transfusiones/      # M4, M5 y M6 (Pruebas, Transfusión y Reacciones)
│   │   └── reportes/           # M7 (Estadísticas)
│   ├── core/                   # Lógica compartida (BaseService, Mixins, etc.)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/         # Componentes UI reutilizables
│   │   ├── pages/              # Vistas completas por módulo
│   │   ├── services/           # Llamadas a API (Axios)
│   │   ├── context/            # Estado global (Auth)
│   │   ├── hooks/              # Lógica de React reutilizable
│   │   └── App.js
│   ├── tailwind.config.js
│   └── package.json
└── docker-compose.yml (opcional para local)