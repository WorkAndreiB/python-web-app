# Frontend

Implemented using HTML, CSS and JavaScript.


It communicates with the backend through asynchronous HTTP requests using the JavaScript Fetch API.

Deployed to CloudFlare using GitHub Actions

## Structure

+ `index.html`: Landing page presenting Beyond Main with thumbnails linking to each app
+ `apps/`: One folder per application (e.g. `apps/password-generator/`)
+ `css/`: Stylesheets for the landing page and individual apps
+ `js/`: JavaScript modules used by the apps

The Task Manager lists tasks and supports creating and editing their title,
description, status, and priority. The task API requires a title of at least
5 characters and a description of at least 10 characters. Use Refresh to
reload the list. Like the password generator, it uses the backend URL in
`js/api.js`; the backend must permit the frontend origin and PUT requests.

## Deployment

Deployed automatically using GitHub Actions and Cloudflare Wrangler.

Workflow:
+ Detects changes affecting the frontend.
+ Checks out the Git repository without initializing submodules.
+ Authenticates with Cloudflare using GitHub Actions secrets.
+ Deploys the frontend's static assets using Wrangler.
+ The deployment is triggered by changes to the frontend or its deployment configuration.


## Start local server for frontend usage
```python -m http.server 5500 --bind 0.0.0.0 --directory <path_to_webpage>```