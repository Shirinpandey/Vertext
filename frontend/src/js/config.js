// OAuth Configuration
// Values are loaded from environment variables
const CONFIG = {
  google: {
    clientId:
      import.meta?.env?.VITE_GOOGLE_CLIENT_ID ||
      process?.env?.VITE_GOOGLE_CLIENT_ID ||
      "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com",
    redirectUri: window.location.origin,
    scope: "openid email profile",
  },
  github: {
    clientId:
      import.meta?.env?.VITE_GITHUB_CLIENT_ID ||
      process?.env?.VITE_GITHUB_CLIENT_ID ||
      "YOUR_GITHUB_CLIENT_ID",
    redirectUri: window.location.origin,
    scope: "read:user user:email",
  },
  // Base URLs for OAuth providers
  authUrls: {
    github: "https://github.com/login/oauth/authorize",
  },
};

// Environment detection
const isProduction =
  window.location.hostname !== "localhost" &&
  window.location.hostname !== "127.0.0.1";

// Export config for use in other modules
window.CONFIG = CONFIG;
