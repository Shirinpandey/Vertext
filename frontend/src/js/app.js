// Main Application Controller
class App {
  constructor() {
    this.loadingSection = null;
    this.isInitialized = false;

    this.initializeApp();
  }

  initializeApp() {
    // Wait for DOM to be ready
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", () => this.setupApp());
    } else {
      this.setupApp();
    }
  }

  setupApp() {
    try {
      // Get DOM elements
      this.loadingSection = document.getElementById("loading-section");

      // Setup event listeners
      this.setupEventListeners();

      // Check URL for OAuth callbacks
      this.handleURLParameters();

      // Check for existing authentication
      this.checkAuthenticationState();

      this.isInitialized = true;
      console.log("App initialized successfully");
    } catch (error) {
      console.error("Error initializing app:", error);
    }
  }

  setupEventListeners() {
    // Authentication events
    window.addEventListener("authSuccess", (e) =>
      this.handleAuthSuccess(e.detail)
    );
    window.addEventListener("authError", (e) => this.handleAuthError(e.detail));
    window.addEventListener("authSignOut", () => this.handleSignOut());

    // UI events
    window.addEventListener("showLoading", () => this.showLoading());
    window.addEventListener("hideLoading", () => this.hideLoading());

    // Browser back/forward navigation
    window.addEventListener("popstate", () => this.handleURLParameters());
  }

  handleURLParameters() {
    const urlParams = new URLSearchParams(window.location.search);

    // GitHub OAuth callback
    const code = urlParams.get("code");
    const state = urlParams.get("state");
    const error = urlParams.get("error");

    if (error) {
      this.handleAuthError(`OAuth error: ${error}`);
      this.clearURLParameters();
      return;
    }

    if (code && state) {
      // Handle GitHub OAuth callback
      this.showLoading();

      if (window.authManager) {
        window.authManager
          .handleGitHubCallback(code, state)
          .then(() => {
            this.clearURLParameters();
          })
          .catch((error) => {
            console.error("GitHub callback error:", error);
            this.handleAuthError("Failed to complete GitHub authentication");
            this.clearURLParameters();
          });
      }
    }
  }

  clearURLParameters() {
    // Clean up URL without page reload
    const url = new URL(window.location);
    url.search = "";
    window.history.replaceState({}, document.title, url);
  }

  checkAuthenticationState() {
    if (window.authManager && window.authManager.isAuthenticated()) {
      const user = window.authManager.getCurrentUser();
      if (user) {
        this.handleAuthSuccess(user);
      }
    } else {
      this.showLoginSection();
    }
  }

  handleAuthSuccess(userData) {
    console.log("Authentication successful:", userData);

    try {
      // Hide loading and login sections
      this.hideLoading();
      this.hideLoginSection();

      // Show profile with user data
      if (window.profileComponent) {
        window.profileComponent.displayUser(userData);
      }

      // Analytics or tracking could go here
      this.trackAuthSuccess(userData.provider);
    } catch (error) {
      console.error("Error handling auth success:", error);
    }
  }

  handleAuthError(error) {
    console.error("Authentication error:", error);

    try {
      // Hide loading
      this.hideLoading();

      // Show login section
      this.showLoginSection();

      // Show error message
      this.showErrorNotification(error);
    } catch (err) {
      console.error("Error handling auth error:", err);
    }
  }

  handleSignOut() {
    console.log("User signed out");

    try {
      // Hide profile section
      if (window.profileComponent) {
        window.profileComponent.hide();
        window.profileComponent.clear();
      }

      // Show login section
      this.showLoginSection();

      // Show success message
      this.showSuccessNotification("Successfully signed out");
    } catch (error) {
      console.error("Error handling sign out:", error);
    }
  }

  showLoading() {
    this.hideAllSections();
    if (this.loadingSection) {
      this.loadingSection.classList.remove("hidden");
      this.loadingSection.classList.add("fade-in");
    }
  }

  hideLoading() {
    if (this.loadingSection) {
      this.loadingSection.classList.add("hidden");
      this.loadingSection.classList.remove("fade-in");
    }
  }

  showLoginSection() {
    this.hideAllSections();
    if (window.loginComponent) {
      window.loginComponent.show();
    }
  }

  hideLoginSection() {
    if (window.loginComponent) {
      window.loginComponent.hide();
    }
  }

  hideAllSections() {
    // Hide all main sections
    const sections = ["login-section", "profile-section", "loading-section"];
    sections.forEach((sectionId) => {
      const section = document.getElementById(sectionId);
      if (section) {
        section.classList.add("hidden");
        section.classList.remove("fade-in");
      }
    });
  }

  showErrorNotification(message) {
    this.showNotification(message, "error");
  }

  showSuccessNotification(message) {
    this.showNotification(message, "success");
  }

  showNotification(message, type = "info") {
    // Create notification element
    const notification = document.createElement("div");
    notification.className = `notification notification-${type}`;

    // Styling
    const backgroundColor = {
      error: "#f8d7da",
      success: "#d4edda",
      info: "#d1ecf1",
    };

    const textColor = {
      error: "#721c24",
      success: "#155724",
      info: "#0c5460",
    };

    const borderColor = {
      error: "#f5c6cb",
      success: "#c3e6cb",
      info: "#b8daff",
    };

    notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${backgroundColor[type]};
            color: ${textColor[type]};
            padding: 15px 20px;
            border-radius: 8px;
            border: 1px solid ${borderColor[type]};
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            z-index: 1000;
            max-width: 300px;
            word-wrap: break-word;
            animation: slideInRight 0.3s ease;
        `;

    notification.textContent = message;

    // Add to DOM
    document.body.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
      if (notification.parentNode) {
        notification.style.animation = "slideOutRight 0.3s ease";
        setTimeout(() => {
          if (notification.parentNode) {
            notification.remove();
          }
        }, 300);
      }
    }, 5000);

    // Add slide animations to CSS if not already present
    this.addNotificationStyles();
  }

  addNotificationStyles() {
    if (!document.getElementById("notification-styles")) {
      const styles = document.createElement("style");
      styles.id = "notification-styles";
      styles.textContent = `
                @keyframes slideInRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOutRight {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            `;
      document.head.appendChild(styles);
    }
  }

  trackAuthSuccess(provider) {
    // Placeholder for analytics tracking
    console.log(`User authenticated with ${provider}`);

    // In a real application, you might send this to analytics:
    // gtag('event', 'login', { method: provider });
    // or
    // analytics.track('User Authenticated', { provider: provider });
  }
}

// Initialize the application
const app = new App();

// Export for global access
window.app = app;
