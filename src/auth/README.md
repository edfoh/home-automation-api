folder to store credentials required to authenticate against google apis to access youtube using oauth2. See [google oauth2 article](https://developers.google.com/identity/protocols/OAuth2) to understand flow.

#### Google API client secret

Store you google client secret key in `client_secret.json`. you can generate one from [developer console](https://console.developers.google.com/)

`This file should never be checked into source control!!`

#### Running this for the first time

When you hit an endpoint that requires google authentication, it will prompt you on the terminal to copy and paste an auth url on your browser. Click `allow` and it should return you a code to enter on the `Enter verification code:` on your terminal. If the browser tab closes, try in chrome `incognito` mode.

After that, a file named `google-user-oauth2.json` should be added to the folder. This file is `git-ignored` so it should not be pushed into github.

#### OAuth2 token storage

After authenticating successfully, a file `google-user-oauth2.json` will be stored in this folder. It contains the access token details, and used to get refresh token upon expiry. It works for offline usage, so you only need to authenticate once.

`This file should never be checked into source control!!`
