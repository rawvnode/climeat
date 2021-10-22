
### Create a Kubernetes secret for storing passwords

```
$ kubectl create secret generic climeat-secret --from-literal=POSTGRES_USER=climeat --from-literal=POSTGRES_PASSWORD=<password>
```

### Update a Kubernetes secret with new value

```
$ kubectl edit secret climeat-secret
```

* This will bring up an editor in your terminal (vim) to edit the secret yaml, you can add any new variables under the data section.
* In order to use the variables from a secret in a pod, you can attach the values in the deployment.yaml for the app, or the statefulset.yaml in the database.  These become environment variables in any container under that workload. like below

```yaml
        env:
          - name: POSTGRES_USER
            valueFrom:
              secretKeyRef:
                name: climeat-secret
                key: POSTGRES_USER
          - name: POSTGRES_PASSWORD
            valueFrom:
              secretKeyRef:
                name: climeat-secret
                key: POSTGRES_PASSWORD
```

### Deploy

**Deploy Everything**

```
$ kubectl apply -k kube
```

**Deploy Database**

```
$ kubectl apply -k kube/database
```

**Deploy App**

```
$ kubectl apply -k kube/app
```

**Force restart**

* If you update the secret for any reason, it won't trigger a redeploy on the workflows so you would have to force it.  If you update the environment variables in deployment.yaml or statefulset.yaml, you can just re apply like above.

```
$ kubectl rollout restart deployments/climeat-api -n climeat
```

```
$ kubectl rollout restart deployments/climeatdb -n climeat
```

** This will cause the database to need re initialized



#### Changes made to app

* app/db/session.py
    - DATABASE_URI now uses environment variables for the database connection, these environment variables must be defined correctly in the app runtime:

    POSTGRES_HOST
    POSTGRES_DB
    POSTGRES_USER
    POSTGRES_PASSWORD

* pyproject.toml
    - Changed richconsole dependency to download v0.25b0 from pypi, upgraded opentelemetry-api and opentelemetry-sdk to 1.6.0 and all other opentelemetry packages to v0.25b0 due to poetry dependency resolver issues