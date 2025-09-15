// Authentication Manager
class AuthManager {
  constructor() {
    this.currentUser = null;
    this.authProvider = null;
    this.googleAuth = null;

    // Initialize Google Auth when DOM is ready
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", () =>
        this.initializeGoogleAuth()
      );
    } else {
      this.initializeGoogleAuth();
    }

    // Check for existing session
    this.checkExistingSession();
  }

  // Initialize Google OAuth
  initializeGoogleAuth() {
    if (typeof google !== "undefined" && google.accounts) {
      google.accounts.id.initialize({
        client_id: CONFIG.google.clientId,
        callback: (response) => this.handleGoogleCallback(response),
        auto_select: false,
        cancel_on_tap_outside: true,
      });
    } else {
      console.warn("Google Identity Services not loaded");
    }
  }

  // Handle Google OAuth callback
  handleGoogleCallback(response) {
    try {
      // Decode the JWT token
      const token = response.credential;
      const payload = this.decodeJWT(token);

      const userData = {
        id: payload.sub,
        name: payload.name,
        email: payload.email,
        picture: payload.picture,
        provider: "google",
      };

      this.setCurrentUser(userData);
      this.notifyAuthSuccess(userData);
    } catch (error) {
      console.error("Error handling Google callback:", error);
      this.notifyAuthError("Failed to process Google authentication");
    }
  }

  // Decode JWT token (simple version - in production use a proper library)
  decodeJWT(token) {
    try {
      const parts = token.split(".");
      const payload = parts[1];
      const decoded = atob(payload.replace(/-/g, "+").replace(/_/g, "/"));
      return JSON.parse(decoded);
    } catch (error) {
      throw new Error("Invalid JWT token");
    }
  }

  // Initialize GitHub OAuth
  signInWithGitHub() {
    const params = new URLSearchParams({
      client_id: CONFIG.github.clientId,
      redirect_uri: CONFIG.github.redirectUri,
      scope: CONFIG.github.scope,
      state: this.generateState(),
    });

    // Store state for verification
    sessionStorage.setItem("github_oauth_state", params.get("state"));

    // Redirect to GitHub OAuth
    window.location.href = `${CONFIG.authUrls.github}?${params}`;
  }

  // Handle GitHub OAuth callback
  async handleGitHubCallback(code, state) {
    try {
      // Verify state parameter
      const storedState = sessionStorage.getItem("github_oauth_state");
      if (state !== storedState) {
        throw new Error("Invalid state parameter");
      }

      // In a real application, you would exchange the code for an access token
      // on your backend server. For demo purposes, we'll simulate this.
      console.log("GitHub OAuth code received:", code);

      // Simulate getting user data (in production, this would be done server-side)
      const userData = await this.simulateGitHubUserData(code);

      this.setCurrentUser(userData);
      this.notifyAuthSuccess(userData);
    } catch (error) {
      console.error("Error handling GitHub callback:", error);
      this.notifyAuthError("Failed to process GitHub authentication");
    }
  }

  // Simulate GitHub user data retrieval (for demo purposes)
  async simulateGitHubUserData(code) {
    // In a real app, you'd exchange the code for an access token server-side
    // and then fetch user data from GitHub API
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          id: "demo_github_user",
          name: "Demo GitHub User",
          email: "demo@github.example",
          picture: "https://github.com/identicons/demo.png",
          provider: "github",
        });
      }, 1000);
    });
  }

  // Generate random state for OAuth security
  generateState() {
    return (
      Math.random().toString(36).substring(2, 15) +
      Math.random().toString(36).substring(2, 15)
    );
  }

  // Set current user and persist session
  setCurrentUser(userData) {
    this.currentUser = userData;
    this.authProvider = userData.provider;

    // Store in sessionStorage for persistence
    sessionStorage.setItem("currentUser", JSON.stringify(userData));
    sessionStorage.setItem("authProvider", userData.provider);
  }

  // Check for existing session
  checkExistingSession() {
    const storedUser = sessionStorage.getItem("currentUser");
    const storedProvider = sessionStorage.getItem("authProvider");

    if (storedUser && storedProvider) {
      try {
        this.currentUser = JSON.parse(storedUser);
        this.authProvider = storedProvider;
        return true;
      } catch (error) {
        console.error("Error parsing stored user data:", error);
        this.clearSession();
      }
    }
    return false;
  }

  // Sign out user
  signOut() {
    // Google sign out
    if (
      this.authProvider === "google" &&
      typeof google !== "undefined" &&
      google.accounts
    ) {
      google.accounts.id.disableAutoSelect();
    }

    // Clear session
    this.clearSession();
    this.notifySignOut();
  }

  // Clear session data
  clearSession() {
    this.currentUser = null;
    this.authProvider = null;
    sessionStorage.removeItem("currentUser");
    sessionStorage.removeItem("authProvider");
    sessionStorage.removeItem("github_oauth_state");
  }

  // Get current user
  getCurrentUser() {
    return this.currentUser;
  }

  // Check if user is authenticated
  isAuthenticated() {
    return this.currentUser !== null;
  }

  // Notify authentication success
  notifyAuthSuccess(userData) {
    const event = new CustomEvent("authSuccess", { detail: userData });
    window.dispatchEvent(event);
  }

  // Notify authentication error
  notifyAuthError(error) {
    const event = new CustomEvent("authError", { detail: error });
    window.dispatchEvent(event);
  }

  // Notify sign out
  notifySignOut() {
    const event = new CustomEvent("authSignOut");
    window.dispatchEvent(event);
  }
}

// Initialize auth manager
const authManager = new AuthManager();

// Export for global access
window.authManager = authManager;
