### Install sample applications

```
kubectl create ns foo
kubectl label namespace foo istio-injection=enabled
kubectl apply -f samples/httpbin/httpbin.yaml -n foo
kubectl apply -f samples/sleep/sleep.yaml -n foo
```


## Test if httpbin can call sleep service
```
kubectl exec $(kubectl get pod -l app=sleep -n foo -o jsonpath={.items..metadata.name}) -c sleep -n foo -- curl http://httpbin.foo:8000/ip -s -o /dev/null -w "%{http_code}\n"
```

## Testing the Authentication Policy

```
 kubectl exec $(kubectl get pod -l app=sleep -n foo -o jsonpath={.items..metadata.name}) -c sleep -n foo -- curl "http://httpbin.foo:8000/headers" -s -o /dev/null -H "Authorization: Bearer invalidToken" -w "%{http_code}\n"
```

## Test without JWT Token

```
kubectl exec $(kubectl get pod -l app=sleep -n foo -o jsonpath={.items..metadata.name}) -c sleep -n foo -- curl "http://httpbin.foo:8000/headers" -s -o /dev/null -w "%{http_code}\n"

```

## Create JWT token with `issuer` and `subject`

```
TOKEN=$(curl https://raw.githubusercontent.com/istio/istio/release-1.19/security/tools/jwt/samples/demo.jwt -s) && echo $TOKEN | cut -d '.' -f2 - | base64 --decode -
```

## Testing the Authorisation Policy with a valid token

```
kubectl exec $(kubectl get pod -l app=sleep -n foo -o jsonpath={.items..metadata.name}) -c sleep -n foo -- curl "http://httpbin.foo:8000/headers" -s -o /dev/null -H "Authorization: Bearer $TOKEN" -w "%{http_code}\n"
```

## Testing the Authorisation Policy without a valid token

```
kubectl exec $(kubectl get pod -l app=sleep -n foo -o jsonpath={.items..metadata.name}) -c sleep -n foo -- curl "http://httpbin.foo:8000/headers" -s -o /dev/null -w "%{http_code}\n"
```

## Create a JWT containing a claim called `groups` with values `group1` and `group2`

```
TOKEN_GROUP=$(curl https://raw.githubusercontent.com/istio/istio/release-1.6/security/tools/jwt/samples/groups-scope.jwt -s) && echo $TOKEN_GROUP | cut -d '.' -f2 - | base64 --decode -
```

## Call  `httpbin` service with above `JWT`

```
kubectl exec $(kubectl get pod -l app=sleep -n foo -o jsonpath={.items..metadata.name}) -c sleep -n foo -- curl "http://httpbin.foo:8000/headers" -s -o /dev/null -H "Authorization: Bearer $TOKEN_GROUP" -w "%{http_code}\n"
```

## Call  JWT that doesn’t contain the `groups` claim

```
kubectl exec $(kubectl get pod -l app=sleep -n foo -o jsonpath={.items..metadata.name}) -c sleep -n foo -- curl "http://httpbin.foo:8000/headers" -s -o /dev/null -H "Authorization: Bearer $TOKEN" -w "%{http_code}\n"
```

