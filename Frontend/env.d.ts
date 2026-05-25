/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_API_URL: string;
    // Añade aquí otras variables que uses, por ejemplo:
    // readonly VITE_SOME_OTHER_KEY: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}