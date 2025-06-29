// main.js
import { UserManager } from 'https://cdn.jsdelivr.net/npm/oidc-client-ts@2.0.2/+esm';

export const userManager = new UserManager({
  authority: "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_E1V33d9fq",
  client_id: "2g17vttj8eeb7fhacugmmfnkeq",
  redirect_uri: "https://d84l1y8p4kdic.cloudfront.net/dashboard.html",
  response_type: "code",
  scope: "openid email phone"
});
