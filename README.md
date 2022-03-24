# nginx with go templates

nginx finally introduced support for templates in their [docker image](https://hub.docker.com/_/nginx) in the tag 1.18.

But these templates use [envsubst](https://www.man7.org/linux/man-pages/man1/envsubst.1.html) which is nice but there are no flow controls, just variable replacement.

This image does nothing else but to replace `envsubst` call with [confgen](https://github.com/fopina/confgen) allowing more powerful templating with [Go templates](https://pkg.go.dev/text/template#hdr-Actions)

## Usage

Usage is all the same as official nginx image: same directories, same enviornment variables, same ways to pass templates. But the expected templates are Go templates instead of envsubst.

The exposed tags in the templates are the ones in [confgen](https://github.com/fopina/confgen).

confgen does provide a build only supporting `env` (with a smaller binary) and a build using [sprig](http://masterminds.github.io/sprig/) with many more tags/functions (and a larger binary).

Builds are available for:
* nginx mainline image
* nginx alpine image

And these are combined with confgen with and without sprig, for those that only need `env` (plus flow control) and rather save a couple of megabytes.

For instance, `nginx:1.19.1` official image is rebuilt into:
* `ghcr.io/surface-security/nginx:1.19.1`
* `ghcr.io/surface-security/nginx:1.19.1-nosprig`
* `ghcr.io/surface-security/nginx:1.19` (if latest 1.19)
* `ghcr.io/surface-security/nginx:1.19-nosprig` (if latest 1.19)

And `nginx:1.19.1-alpine` into:
* `ghcr.io/surface-security/nginx:1.19.1-alpine`
* `ghcr.io/surface-security/nginx:1.19.1-nosprig-alpine`
* `ghcr.io/surface-security/nginx:1.19-alpine` (if latest 1.19)
* `ghcr.io/surface-security/nginx:1.19-nosprig-alpine` (if latest 1.19)

### Debugging templates

When the generated .conf file has errors, nginx will report the line numbers in the templated file (not the template).

As nginx container will die when there are errors, you have three options for quickly looking at the templating results:
* Download [confgen](https://github.com/fopina/confgen) to your machine and run `confgen TEMPLATE_FILE`
* Use this docker image calling config: `docker run -v TEMPLATE:/my.template ghcr.io/surface-security/nginx:1.19-alpine confgen /my.template`
* Start the container with `-e NGINX_TEMPLATE_DEBUG=1` and the startup script will dump the generated files in the logs/stdout


### Examples

Quick example where Go templating flow controls are useful (versus simpler envsubst):
* configuration that will lock content based on server_name if one is defined else allow anything

Template:

```
{{ if ne ("ALLOWED_HOSTS"|env) "" }}
server {
  listen 8080 default_server;
  return 444;
}
{{ end }}

server {
  listen 8080 deferred;

  {{ if ne ("ALLOWED_HOSTS"|env) "" }}
  server_name {{ "ALLOWED_HOSTS" | env | replace "," " " }};
  {{ end }}

  location / {
    # ... rest of the config
  }
}
```

```
$ docker run -v $(pwd)/example.template:/my.template:ro ghcr.io/surface-security/nginx:1.19 confgen /my.template
server {
  listen 8080 deferred;



  location / {
    # ... rest of the config
  }
}
```

```
$ docker run -v $(pwd)/example.template:/my.template:ro -e ALLOWED_HOSTS=my.example.com,example.com ghcr.io/surface-security/nginx:1.19-alpine confgen /my.template
server {
  listen 8080 default_server;
  return 444;
}


server {
  listen 8080 deferred;


  server_name my.example.com example.com;


  location / {
    # ... rest of the config
  }
}
```
