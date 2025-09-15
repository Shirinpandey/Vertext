# Vertext OAuth Frontend

A simple, barebones frontend application that implements OAuth authentication with Google and GitHub. Users can sign in with their preferred account and see their profile information displayed.

## Features

- 🔐 OAuth authentication with Google and GitHub
- 👤 User profile display with name, email, and avatar
- 🎨 Clean, responsive UI design
- 🔄 Session persistence
- ♿ Accessibility support
- 📱 Mobile-friendly design

## Project Structure

```
frontend/
├── src/
│   ├── index.html          # Main HTML file
│   ├── css/
│   │   └── styles.css      # Application styles
│   ├── js/
│   │   ├── config.js       # OAuth configuration
│   │   ├── auth.js         # Authentication manager
│   │   └── app.js          # Main application logic
│   └── components/
│       ├── login.js        # Login component
│       └── profile.js      # Profile component
├── package.json            # Dependencies and scripts
└── README.md              # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure OAuth Applications

#### Google OAuth Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" and create an OAuth 2.0 Client ID
5. Add your domain to authorized JavaScript origins:
   - For development: `http://localhost:3000`
   - For production: `https://yourdomain.com`
6. Add authorized redirect URIs:
   - For development: `http://localhost:3000`
   - For production: `https://yourdomain.com`
7. Copy the Client ID

#### GitHub OAuth Setup

1. Go to your GitHub Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Fill in the application details:
   - Application name: `Vertext OAuth Demo`
   - Homepage URL: `http://localhost:3000` (or your domain)
   - Authorization callback URL: `http://localhost:3000` (or your domain)
4. Click "Register application"
5. Copy the Client ID (keep the Client Secret secure)

### 3. Update Configuration

Edit `src/js/config.js` and replace the placeholder values:

```javascript
const CONFIG = {
  google: {
    clientId: "YOUR_ACTUAL_GOOGLE_CLIENT_ID.apps.googleusercontent.com",
    redirectUri: window.location.origin,
    scope: "openid email profile",
  },
  github: {
    clientId: "YOUR_ACTUAL_GITHUB_CLIENT_ID",
    redirectUri: window.location.origin,
    scope: "read:user user:email",
  },
  // ... rest of config
};
```

### 4. Run the Application

Start the development server:

```bash
npm run dev
```

This will start a local server at `http://localhost:3000` and automatically open it in your browser.

For production or manual testing:

```bash
npm start
```

## Usage

1. Open the application in your browser
2. Click either "Sign in with Google" or "Sign in with GitHub"
3. Complete the OAuth flow in the popup/redirect
4. Your profile information will be displayed
5. Click "Sign Out" to end the session

## Technical Details

### Authentication Flow

#### Google OAuth

- Uses Google Identity Services (One Tap/Sign-In)
- Handles JWT token decoding for user information
- Supports both popup and redirect flows

#### GitHub OAuth

- Implements standard OAuth 2.0 authorization code flow
- Requires server-side token exchange (simulated in demo)
- Includes CSRF protection with state parameter

### Security Features

- CSRF protection with random state parameters
- Secure session storage
- Input validation and error handling
- XSS protection through proper DOM manipulation

### Browser Compatibility

- Modern browsers supporting ES6+ features
- Graceful degradation for older browsers
- Mobile-responsive design

## Customization

### Styling

Edit `src/css/styles.css` to customize the appearance. The CSS uses CSS custom properties for easy theming.

### Adding More Providers

1. Add provider configuration to `config.js`
2. Extend the `AuthManager` class in `auth.js`
3. Add corresponding buttons to the HTML
4. Update the login component

### Server-Side Integration

For production use, implement proper server-side endpoints for:

- Token exchange for GitHub OAuth
- User data fetching
- Session management
- Security validation

## Deployment

### Static Hosting

Since this is a client-side application, it can be deployed to any static hosting service:

- **Netlify**: Drag and drop the `src/` folder
- **Vercel**: Connect your GitHub repository
- **GitHub Pages**: Push to a `gh-pages` branch
- **AWS S3**: Upload files to an S3 bucket with website hosting

### Important Notes for Production

1. **HTTPS Required**: OAuth providers require HTTPS for production
2. **Domain Whitelist**: Update OAuth app settings with your production domain
3. **Environment Variables**: Consider using environment variables for client IDs
4. **Server Backend**: Implement proper backend for token exchange and validation

## Troubleshooting

### Common Issues

**Google Sign-In not working:**

- Check if the Client ID is correct
- Verify domain is added to authorized origins
- Ensure HTTPS is used in production

**GitHub Sign-In not working:**

- Verify Client ID matches your GitHub OAuth app
- Check authorization callback URL
- Ensure popup blockers are disabled

**Profile not displaying:**

- Check browser console for JavaScript errors
- Verify user data is being received correctly
- Check if profile component is loaded

### Debug Mode

To enable debug logging, open browser console and run:

```javascript
localStorage.setItem("debug", "true");
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:

- Check the browser console for error messages
- Review OAuth provider documentation
- Ensure all setup steps are completed correctly
