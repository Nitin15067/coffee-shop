/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'nitin15067.us', // the auth0 domain prefix
    audience: 'staff', // the audience set for the auth0 app
    clientId: '9FYdt3aHRIeKJ7RHgVIYIuQ89mzn4KXv', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running ionic application.
  }
};
