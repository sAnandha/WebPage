
import { UserManager } from "https://cdn.jsdelivr.net/npm/oidc-client-ts/+esm";

const cognitoAuthConfig = {
  authority: "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_E1V33d9fq",
  client_id: "2g17vttj8eeb7fhacugmmfnkeq",
  redirect_uri: "https://d84l1y8p4kdic.cloudfront.net/dashboard.html",
  response_type: "code",
  scope: "openid email phone",
};

export const userManager = new UserManager(cognitoAuthConfig);

export async function signOutRedirect() {
  const logoutUri = "https://d84l1y8p4kdic.cloudfront.net";
  const cognitoDomain = "https://us-east-1e1v33d9fq.auth.us-east-1.amazoncognito.com";
  window.location.href = \`\${cognitoDomain}/logout?client_id=\${cognitoAuthConfig.client_id}&logout_uri=\${encodeURIComponent(logoutUri)}\`;
}
