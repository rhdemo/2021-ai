# S2I-flask-app

```
▶ oc new-app https://github.com/sub-mod/s2i-flask-notebook.git -l name=s2i-flask-app
--> Found image c76c973 (6 weeks old) in image stream "openshift/python" under tag "3.8-ubi8" for "python"

    Python 3.8
    ----------
    Python 3.8 available as container is a base platform for building and running various Python 3.8 applications and frameworks. Python is an easy to learn, powerful programming language. It has efficient high-level data structures and a simple but effective approach to object-oriented programming. Python's elegant syntax and dynamic typing, together with its interpret
{
ed nature, make it an ideal language for scripting and rapid application development in many areas on most platforms.

    Tags: builder, python, python38, python-38, rh-python38

    * The source repository appears to match: python
    * A source build using source code from https://github.com/sub-mod/s2i-flask-notebook.git will be created
      * The resulting image will be pushed to image stream tag "s2i-flask-notebook:latest"
      * Use 'oc start-build' to trigger a new build
    * This image will be deployed in deployment config "s2i-flask-notebook"
    * Port 8080/tcp will be load balanced by service "s2i-flask-notebook"
      * Other containers can access this service through the hostname "s2i-flask-notebook"

--> Creating resources ...
    imagestream.image.openshift.io "s2i-flask-notebook" created
    buildconfig.build.openshift.io "s2i-flask-notebook" created
    deploymentconfig.apps.openshift.io "s2i-flask-notebook" created
    service "s2i-flask-notebook" created
--> Success
    Build scheduled, use 'oc logs -f bc/s2i-flask-notebook' to track its progress.
    Application is not exposed. You can expose services to the outside world by executing one or more of the commands below:
     'oc expose svc/s2i-flask-notebook'
    Run 'oc status' to view your app.
```

```
▶ oc expose svc/s2i-flask-notebook -l name=s2i-flask-app
route.route.openshift.io/s2i-flask-notebook exposed
```

```
▶ oc get routes
NAME                 HOST/PORT                                                               PATH   SERVICES             PORT       TERMINATION   WILDCARD
s2i-flask-notebook   s2i-flask-notebook-test.apps.internal.openshiftapps.com          s2i-flask-notebook   8080-tcp                 None
```

```
▶ curl http://s2i-flask-notebook-test.apps.internal.openshiftapps.com/status
{"status":"ok"}
```

```
▶ curl -X POST -d @data.json http://2i-flask-notebook-test.apps.internal.openshiftapps.com/prediction
{"prediction":"not implemented"}
```

```
▶ oc delete all -l name=s2i-flask-app
pod "s2i-flask-notebook-1-kqdls" deleted
replicationcontroller "s2i-flask-notebook-1" deleted
service "s2i-flask-notebook" deleted
deploymentconfig.apps.openshift.io "s2i-flask-notebook" deleted
buildconfig.build.openshift.io "s2i-flask-notebook" deleted
build.build.openshift.io "s2i-flask-notebook-1" deleted
imagestream.image.openshift.io "s2i-flask-notebook" deleted
route.route.openshift.io "s2i-flask-notebook" deleted
```