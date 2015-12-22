# Django REST framework example

## Directory structure
	
<pre>
	/var/www/mysite.com/
		.gitignore
		manage.py
		fabfile.py
		robots.txt
		package.json
		conf/
			nginx/
				nginx.dev.conf
				nginx.prod.conf
			uwsgi/
				mysite.ini
				uwsgi.conf
			pip/
				requirements.txt
			sensitive-fake/
				configuration.ini
				remote_server.pem
		logs/
		mysite/
			__init__.py
			urls.py
			wsgi.py
			apps/
				main/
					__init__.py
					admin.py
					models.py
					permissions.py
					seliarizers.py
					tests.py
					urls.py
					views.py
				utils/
					__init__.py
					cron.py
					redis.py
					utilities.py
			settings/
				__init__.py
				base.py
				dev.py
				prod.py
			templates/
				base.html
				index.html
				404.html
				503.html
			static/
				css/
					styles.scss
					styles.map
					styles.css
				js/
					index.js
					webpack.config.js
					module/
							obtainAuthToken.js
							verifyAuthToken.js
							setAuthToken.js
							refreshAuthToken.js
							clearAuthToken.js
							setCSRFToken.js
					dist/
							bundle.js
							vendor.bundle.js
</pre>


## Installation


## Customization

#### Rename project and configure basic settings

~~~~
$ mv django-rest-framework-example/ /var/www/{YOUR PROJECT NAME}.com/
$ cd /var/www/{YOUR PROJECT NAME}.com/
$ mv mysite/ {YOUR PROJECT NAME}/
~~~~

- Let `{PROJECT PATH}` as `/var/www/{YOUR PROJECT NAME}.com/`

~~~~
$ cd {PROJECT PATH}/conf/uwsgi/
$ mv mysite.ini {YOUR PROJECT NAME}.ini
$ vi {YOUR PROJECT NAME}.ini

	:%s/mysite/{YOUR PROJECT NAME}/g

$ cd {PROJECT PATH}/conf/nginx/
$ vi nginx.dev.conf nginx.prod.conf

	:%s/mysite/{YOUR PROJECT NAME}/g
~~~~

-	Edit value of `worker_processes` to `grep processor /proc/cpuinfo | wc -l`
-	Edit value of `worker_connections` to `ulimit -n`
-	Commentify `Redirect HTTP to HTTPS` block if you will not use SSL
-	Commentify `Redirect www to non-www` block if you will not redirect `www` to `non-www`

~~~~
$ cd {PROJECT PATH}/
$ vi manage.py
~~~~

- Select development mode or production mode

~~~~
$ cd {PROJECT PATH}/{PROJECT NAME}/
$ vi wsgi.py
~~~~

- Select development mode or production mode

#### Fill out sensitive data

~~~~
$ cd {PROJECT PATH}/conf/
$ cp -R sensitive-data/ sensitive/
$ vi configuration.ini [Fill out variables]
$ vi remote_server.pem [Fill out public certificate of remote server]
~~~~
