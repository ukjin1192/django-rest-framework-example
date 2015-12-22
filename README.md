# Django REST framework example (Under construction now)

## Directory structure
	
<pre>
	/var/www/budafoo.com/
		.gitignore
		manage.py
		fabfile.py
		robots.txt
		conf/
			nginx/
				nginx.dev.conf
				nginx.prod.conf
			uwsgi/
				budafoo.ini
				uwsgi.conf
			pip/
				requirements.txt
			sensitive-fake/
				configuration.ini
				remote_server.pem
		logs/
		budafoo/
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
</pre>


## Things that should be customized

#### Rename project and configure basic settings

~~~~
$ mv django-rest-framework-example/ /var/www/{YOUR PROJECT NAME}.com/
$ cd /var/www/{YOUR PROJECT NAME}.com/
$ mv budafoo/ {YOUR PROJECT NAME}/
~~~~

- Let `{PROJECT PATH}` as `/var/www/{YOUR PROJECT NAME}.com/`

~~~~
$ cd {PROJECT PATH}/conf/uwsgi/
$ mv budafoo.ini {YOUR PROJECT NAME}.ini
$ vi {YOUR PROJECT NAME}.ini

	:%s/budafoo/{YOUR PROJECT NAME}/g

$ cd {PROJECT PATH}/conf/nginx/
$ vi nginx.dev.conf nginx.prod.conf

	:%s/budafoo/{YOUR PROJECT NAME}/g
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
