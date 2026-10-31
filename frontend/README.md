# Frontend

Implemented using HTML, CSS and JavaScript.


It communicates with the backend through asynchronous HTTP requests using the JavaScript Fetch API.

Deployed to CloudFlare using GitHub Actions

## Structure

+ `index.html`: Landing page presenting Beyond Main with thumbnails linking to each app
+ `apps/`: One folder per application (e.g. `apps/password-generator/`)
+ `css/`: Stylesheets (`home.css` for the landing page, `style.css` for the apps)
+ `js/`: JavaScript modules used by the apps

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