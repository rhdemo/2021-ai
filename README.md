# BATAAI

## Deploy 
```
▶ oc new-app https://github.com/sub-mod/bataai.git -l name=bataai
```

```
▶ oc expose svc/bataai -l name=bataai
route.route.openshift.io/bataai exposed
```

```
▶ oc get routes
NAME     HOST/PORT                                                   PATH   SERVICES   PORT       TERMINATION   WILDCARD
bataai   bataai-test.apps.rhods-internal.openshiftapps.com          bataai     8080-tcp                 None
```

```
▶ curl http://bataai-test.apps.rhods-internal.ju9j.p1.openshiftapps.com/status
{"status":"ok"}
```

## Predict 
```
//1 - MISS
//2 - HIT
//-1 - unplayed
▶ curl -X POST -H "Content-Type: application/json" -d @data.json http://bataai-test.apps.rhods-internal.ju9j.p1.openshiftapps.com/prediction
{"prob":[[8,11,12,11,8],[11,14,15,14,11],[12,15,16,15,12],[11,14,15,14,11],[8,11,12,11,8]],"x":2,"y":2}
```

## Update code 
```
▶ oc start-build bataai
```

## Cleanup 
```
▶ oc delete all -l name=bataai
```