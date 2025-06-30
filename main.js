// main.js
import { UserManager } from "https://cdn.jsdelivr.net/npm/oidc-client-ts/+esm";
// Cognito OIDC configuration
const cognitoAuthConfig = {
  authority: "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_E1V33d9fq", // Your Cognito user pool's issuer URL
  client_id: "2g17vttj8eeb7fhacugmmfnkeq", // Your App Client ID
  redirect_uri: "https://main.de43hd7rcr7qe.amplifyapp.com/dashboard.html", // Where Cognito redirects after login
  response_type: "code", // Authorization Code Flow
  scope: "openid email profile" // Request ID token + user info
};
// Create an instance of UserManager
export const userManager = new UserManager({
  ...cognitoAuthConfig
});
// Optional: Sign-out function that redirects to Cognito logout endpoint
export async function signOutRedirect() {
  const clientId = cognitoAuthConfig.client_id;
  const logoutUri = "https://main.de43hd7rcr7qe.amplifyapp.com"; // After logout, return here
  const cognitoDomain = "https://us-east-1e1v33d9fq.auth.us-east-1.amazoncognito.com"; // Cognito Hosted UI Domain

  window.location.href = ${cognitoDomain}/logout?client_id=${clientId}&logout_uri=${encodeURIComponent(logoutUri)};
}
