import { UserManager } from "oidc-client-ts";

const cognitoAuthConfig = {
    authority: "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_E1V33d9fq",
    client_id: "2g17vttj8eeb7fhacugmmfnkeq",
    redirect_uri: "https://main.de43hd7rcr7qe.amplifyapp.com/dashboard.html",
    response_type: "code",
    scope: "email openid phone"
};

export const userManager = new UserManager({
    ...cognitoAuthConfig,
});

export async function signOutRedirect () {
    const logoutUri = "https://main.de43hd7rcr7qe.amplifyapp.com/";
    const cognitoDomain = "https://us-east-1e1v33d9fq.auth.us-east-1.amazoncognito.com";
    window.location.href = `${cognitoDomain}/logout?client_id=2g17vttj8eeb7fhacugmmfnkeq&logout_uri=${encodeURIComponent(logoutUri)}`;
}
