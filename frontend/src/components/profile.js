// Profile Component
class ProfileComponent {
  constructor() {
    this.profileSection = null;
    this.userAvatar = null;
    this.userName = null;
    this.userEmail = null;
    this.authProvider = null;
    this.logoutButton = null;

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
    this.profileSection = document.getElementById("profile-section");
    this.userAvatar = document.getElementById("avatar-img");
    this.userName = document.getElementById("user-name");
    this.userEmail = document.getElementById("user-email");
    this.authProvider = document.getElementById("auth-provider");
    this.logoutButton = document.getElementById("logout-btn");

    if (!this.profileSection || !this.userName || !this.logoutButton) {
      console.error("Profile component elements not found");
      return;
    }

    // Setup event listeners
    this.setupEventListeners();
  }

  setupEventListeners() {
    // Logout button
    this.logoutButton.addEventListener("click", () => this.handleLogout());

    // Keyboard accessibility for logout button
    this.logoutButton.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        this.handleLogout();
      }
    });
  }

  handleLogout() {
    // Show confirmation dialog
    const confirmed = confirm("Are you sure you want to sign out?");

    if (confirmed) {
      try {
        // Use auth manager to handle logout
        if (window.authManager) {
          window.authManager.signOut();
        } else {
          console.error("Auth manager not available");
          // Fallback: dispatch sign out event
          const event = new CustomEvent("authSignOut");
          window.dispatchEvent(event);
        }
      } catch (error) {
        console.error("Logout error:", error);
      }
    }
  }

  displayUser(userData) {
    try {
      // Update user name
      if (this.userName) {
        this.userName.textContent = userData.name || "Welcome!";
      }

      // Update user email
      if (this.userEmail) {
        this.userEmail.textContent = userData.email || "";
        this.userEmail.style.display = userData.email ? "block" : "none";
      }

      // Update user avatar
      if (this.userAvatar && userData.picture) {
        this.userAvatar.src = userData.picture;
        this.userAvatar.alt = `${userData.name}'s avatar`;
        this.userAvatar.onerror = () => {
          // Fallback to default avatar on error
          this.setDefaultAvatar(userData.name);
        };
      } else {
        this.setDefaultAvatar(userData.name);
      }

      // Update auth provider
      if (this.authProvider) {
        const providerText = this.getProviderDisplayName(userData.provider);
        this.authProvider.textContent = `Signed in with ${providerText}`;
      }

      // Show profile section
      this.show();
    } catch (error) {
      console.error("Error displaying user data:", error);
    }
  }

  setDefaultAvatar(name) {
    if (this.userAvatar) {
      // Create a simple text-based avatar
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      canvas.width = 80;
      canvas.height = 80;

      // Background color based on name
      const colors = [
        "#667eea",
        "#764ba2",
        "#f093fb",
        "#f5576c",
        "#4facfe",
        "#00f2fe",
      ];
      const colorIndex = name ? name.charCodeAt(0) % colors.length : 0;

      ctx.fillStyle = colors[colorIndex];
      ctx.fillRect(0, 0, 80, 80);

      // Text
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 32px Arial";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";

      const initials = this.getInitials(name);
      ctx.fillText(initials, 40, 40);

      this.userAvatar.src = canvas.toDataURL();
      this.userAvatar.alt = `${name}'s avatar`;
    }
  }

  getInitials(name) {
    if (!name) return "?";

    const parts = name.trim().split(" ");
    if (parts.length === 1) {
      return parts[0].charAt(0).toUpperCase();
    } else {
      return (
        parts[0].charAt(0) + parts[parts.length - 1].charAt(0)
      ).toUpperCase();
    }
  }

  getProviderDisplayName(provider) {
    switch (provider) {
      case "google":
        return "Google";
      case "github":
        return "GitHub";
      default:
        return provider || "Unknown";
    }
  }

  show() {
    if (this.profileSection) {
      this.profileSection.classList.remove("hidden");
      this.profileSection.classList.add("fade-in");
    }
  }

  hide() {
    if (this.profileSection) {
      this.profileSection.classList.add("hidden");
      this.profileSection.classList.remove("fade-in");
    }
  }

  clear() {
    // Clear user data from UI
    if (this.userName) this.userName.textContent = "Welcome!";
    if (this.userEmail) this.userEmail.textContent = "";
    if (this.authProvider) this.authProvider.textContent = "";
    if (this.userAvatar) this.userAvatar.src = "";
  }
}

// Initialize profile component
const profileComponent = new ProfileComponent();

// Export for global access
window.profileComponent = profileComponent;
