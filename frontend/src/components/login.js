// Login Component
class LoginComponent {
  constructor() {
    this.googleButton = null;
    this.githubButton = null;
    this.loginSection = null;

    this.initializeComponent();
  }

  initializeComponent() {
    // Wait for DOM to be ready
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", () =>
        this.setupComponent()
      );
    } else {
      this.setupComponent();
    }
  }

  setupComponent() {
    // Get DOM elements
    this.loginSection = document.getElementById("login-section");
    this.googleButton = document.getElementById("google-signin-btn");
    this.githubButton = document.getElementById("github-signin-btn");

    if (!this.loginSection || !this.googleButton || !this.githubButton) {
      console.error("Login component elements not found");
      return;
    }

    // Setup event listeners
    this.setupEventListeners();

    // Initialize Google Sign-In button
    this.initializeGoogleButton();
  }

  setupEventListeners() {
    // Google Sign-In button
    this.googleButton.addEventListener("click", () =>
      this.handleGoogleSignIn()
    );

    // GitHub Sign-In button
    this.githubButton.addEventListener("click", () =>
      this.handleGitHubSignIn()
    );

    // Keyboard accessibility
    this.googleButton.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        this.handleGoogleSignIn();
      }
    });

    this.githubButton.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        this.handleGitHubSignIn();
      }
    });

    // Make buttons focusable for accessibility
    this.googleButton.setAttribute("tabindex", "0");
    this.githubButton.setAttribute("tabindex", "0");
  }

  initializeGoogleButton() {
    // Try to render Google One Tap or Sign-In button
    if (typeof google !== "undefined" && google.accounts) {
      try {
        // Alternative: render a proper Google Sign-In button
        google.accounts.id.renderButton(
          document.getElementById("google-signin-btn"),
          {
            theme: "outline",
            size: "large",
            type: "standard",
            shape: "rectangular",
            text: "signin_with",
            logo_alignment: "left",
            width: "100%",
          }
        );
      } catch (error) {
        console.log("Using custom Google button styling");
        // Keep the custom button if Google button rendering fails
      }
    }
  }

  handleGoogleSignIn() {
    if (typeof google !== "undefined" && google.accounts) {
      try {
        // Show loading state
        this.showLoadingState();

        // Prompt Google Sign-In
        google.accounts.id.prompt((notification) => {
          if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
            // If prompt fails, fallback to popup
            console.log("Google One Tap not available, using popup");
            this.hideLoadingState();
          }
        });
      } catch (error) {
        console.error("Google Sign-In error:", error);
        this.hideLoadingState();
        this.showErrorMessage("Google Sign-In is not available");
      }
    } else {
      this.showErrorMessage("Google Sign-In is not loaded");
    }
  }

  handleGitHubSignIn() {
    try {
      // Show loading state
      this.showLoadingState();

      // Use auth manager to handle GitHub OAuth
      if (window.authManager) {
        window.authManager.signInWithGitHub();
      } else {
        throw new Error("Auth manager not available");
      }
    } catch (error) {
      console.error("GitHub Sign-In error:", error);
      this.hideLoadingState();
      this.showErrorMessage("GitHub Sign-In failed");
    }
  }

  showLoadingState() {
    // Dispatch event to show loading section
    const event = new CustomEvent("showLoading");
    window.dispatchEvent(event);
  }

  hideLoadingState() {
    // Dispatch event to hide loading section
    const event = new CustomEvent("hideLoading");
    window.dispatchEvent(event);
  }

  showErrorMessage(message) {
    // Create and show error notification
    const errorDiv = document.createElement("div");
    errorDiv.className = "error-message";
    errorDiv.style.cssText = `
            background: #f8d7da;
            color: #721c24;
            padding: 12px;
            border-radius: 8px;
            margin-top: 15px;
            text-align: center;
            border: 1px solid #f5c6cb;
            animation: fadeIn 0.3s ease;
        `;
    errorDiv.textContent = message;

    // Insert error message
    const oauthButtons = document.querySelector(".oauth-buttons");
    if (oauthButtons) {
      oauthButtons.appendChild(errorDiv);

      // Auto-remove after 5 seconds
      setTimeout(() => {
        if (errorDiv.parentNode) {
          errorDiv.remove();
        }
      }, 5000);
    }
  }

  show() {
    if (this.loginSection) {
      this.loginSection.classList.remove("hidden");
      this.loginSection.classList.add("fade-in");
    }
  }

  hide() {
    if (this.loginSection) {
      this.loginSection.classList.add("hidden");
      this.loginSection.classList.remove("fade-in");
    }
  }
}

// Initialize login component
const loginComponent = new LoginComponent();

// Export for global access
window.loginComponent = loginComponent;
