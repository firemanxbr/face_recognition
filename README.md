# Introduction

This is the documentation regarding the personal project to calculate the value of the average face embedding vector across a large dataset of faces/photos.

## Architecture

![Architecture](doc/images/architecture.png)
This is the first release of the architecture proposal. Each box have an indicator that defines the factor of scalability, for example, 1/1 - [ ] Minimal/Maximum;

**Note:** Regarding of this project, was used a MacBook Pro, the tools mentioned in this document, and the code created respecting the requirements received.

### RabbitMQ

The first component is the RabbitMQ service that works as a Broker, receiving messages to share between **Producer** and **Workers**. RabbitMQ is the base of data consumed by **Flower** also. To the future is possible to clusterized this service to attend the 1/n salability requirement but for reasons of resources in this challenge will use only one container.

### Workers

The workers have the goal to process any task that was sent to them. It is the first service used in this challenge to accelerate, parallelizing the tasks of the challenge attending the scalability requirement. Was used 4 containers to process face recognition.

### Producer

The producer is only a container that will download the dataset, validate, extract, and submit each photo as a task. After the process of photos are finished the producer can calculate the average of all faces. To this challenge was an option to don't parallelize this container but in the future is possible to elevate the scalability factor of this service.

### Flower

The Flower is used to allow the operators to have more information about what's in process with a bunch of substantial metrics. Observability is the best description of what this tool can offer to us.

## REQUIREMENTS

The requirements necessary to reproduce, test or run the solution:

* MacBookPro with minimal 16gb of RAM and 4 CPUs running the macOS Mojave
* VirtualBox
* Minikube
* Docker
* Minimal Python 3.6

**Node:** I'll not mention the standard configuration of the tools. All custom configurations will be included below.

## Deployment

The first action to reproduce this workforce will be clone the repositorie below:

https://github.com/firemanxbr/face_recognition

After attending all requirements, installing and configuring the tools using the official documentation from each place, we can start our kubernetes/minikube.

### Minikube

```code
$ minikube start - [ ]- [ ]vm- [ ]driver virtualbox - [ ]- [ ]disk- [ ]size 50G - [ ]- [ ]cpus 4 - [ ]- [ ]memory 12000 - [ ]v=10
...
🚜  Pulling images ...
🚀  Launching Kubernetes ...
⌛  Verifying: apiserver proxy etcd scheduler controller dns
🏄  Done! kubectl is now configured to use "minikube"
```

Getting the IP used to open the tools of our architecture:

```code
$ minikube status
host: Running
kubelet: Running
apiserver: Running
kubectl: Correctly Configured: pointing to minikube- [ ]vm at 192.168.99.103
```

The IP used on minikube- [ ]vm will be used to access the web interfaces in this project.

We can use the minikube dashboard to analyze the use of our resources by kubernetes:

```code
$ minikube dashboard
🔌  Enabling dashboard ...
🤔  Verifying dashboard health ...
🚀  Launching proxy ...
🤔  Verifying proxy health ...
🎉  Opening http://127.0.0.1:49926/api/v1/namespaces/kube- [ ]system/services/http:kubernetes- [ ]dashboard:/proxy/ in your default browser...
```

### Kubernetes/Minikube

Inside of the repository will exist a folder named **kube/**, where will allow us to deploy our containers:

```code
$ kubectl apply - [ ]f infra.yaml
service/rabbitmq created
deployment.extensions/rabbitmq created
persistentvolume/task- [ ]pv- [ ]volume unchanged
persistentvolumeclaim/task- [ ]pv- [ ]claim unchanged
```

Please wait the RabbitMQ will be running to continue deployment the other containers. How to check the RabbitMQ container?

```code
$ kubectl get pods
NAME                        READY   STATUS    RESTARTS   AGE
rabbitmq- [ ]7d4bff7b86- [ ]vscjw   1/1     Running   0          95s
```

When RabbitMQ(The Broker) it's running and ready to use we can deploy the workers and the flower:

Workers:

```code
$ kubectl apply - [ ]f worker.yaml
deployment.extensions/worker created
```

Flower:

```code
$ kubectl apply - [ ]f flower.yaml
deployment.extensions/celery- [ ]flower created
service/celery- [ ]flower created
```

### Flower

The web interface of Flower can be accesible using the IP of minikube VM, for example:

http://192.168.99.109:30555/dashboard

![Flower](doc/images/flower1.png)

Using this tool is possible to see each task sent by **Producer**, in process or finished by **Workers**.

### Minikube Dashboard

The Minikube Dashboard is used to management the containers and see the logs inside of a container. In this challenge this access is so important.

![Dashboard](doc/images/minikube- [ ]dashboard.png)

### Start the process

To start the process will be necessary only deploy the **Producer** container because it is responsable to send tasks to the RabbitMQ/Celery and receive the results from the Workers. How to start?

```code
kubectl apply - [ ]f producer.yaml
deployment.extensions/producer created
```

Afert that is possible to see all containers in perfect operation:

```code
$ kubectl get pods
NAME                             READY   STATUS    RESTARTS   AGE
celery- [ ]flower- [ ]7dcc9f95b8- [ ]4l8bh   1/1     Running   0          27m
producer- [ ]5447bdc884- [ ]b8vbz        1/1     Running   0          13m
rabbitmq- [ ]7d4bff7b86- [ ]ncvw4        1/1     Running   0          28m
worker- [ ]d8c475f68- [ ]cv8dw           1/1     Running   0          23m
worker- [ ]d8c475f68- [ ]n9ghb           1/1     Running   0          23m
worker- [ ]d8c475f68- [ ]qztln           1/1     Running   0          23m
worker- [ ]d8c475f68- [ ]r4hx2           1/1     Running   0          23m
```

### Checking the Results/Logs

The image below is the logs of the **producer** container:

![Producer](doc/images/producer-logs.png)

Into the Flower web interface is possible to check in details all tasks sent, received, processed and returned to the **producer** container:

![Flower](doc/images/flower-numbers.png)

### Docker Images

The best image to support the **face_recognition** library was the **CentOs Linux**. All images generated to this challange are in the public Docker Hub:

https://cloud.docker.com/u/firemanxbr/repository/docker/firemanxbr/veriff

## Report and metrics reached

Following below the numbers generated. With more time and resources will be substantially increased these numbers could be better:

The Logfile it's available here: [Logfile in Text](logs-from-producer-in-producer-7977b4b95c-f8lhl.txt)

| Total of Photos | Failed(Exceptions/Hardware/Libraries) | Succeeded | Total Time to Finish |
| :-------: | :------------: | :-------------: | :--------------: |
| 13.233  | 63  | 13.170 | ~ 20 min |

```code
############################################################
Jul 04 2019 17:39:35:1562261975 - Starting Producer Process...
Jul 04 2019 17:41:45:1562262105 - Starting Creating Tasks...
Jul 04 2019 17:42:21:1562262141 - Total of Tasks Created: 13233
Jul 04 2019 17:42:21:1562262141 - Getting Tasks Done...
Jul 04 2019 17:59:26:1562263166 - Total of Tasks Finished: 13233
Jul 04 2019 17:59:26:1562263166 - Calculating Average Vectors...
Jul 04 2019 17:59:26:1562263166 - Total of Photos Processed: 13170
Jul 04 2019 17:59:26:1562263166 - Result of calculation the average of values:
[-9.14782873e-02  1.16529173e-01  1.24739484e-02 -4.87357295e-03
 -7.64022485e-02 -5.12338763e-03 -5.91263196e-03 -1.20411217e-01
  8.06266393e-02 -1.30041725e-02  2.19767796e-01 -6.30949522e-02
 -3.00631403e-01 -4.73570373e-02 -1.53999909e-02  1.29851877e-01
 -1.93632883e-01 -7.03056175e-02 -1.81564300e-01 -6.77238636e-02
 -3.48251773e-02  2.89526970e-02  4.01914614e-02 -1.24878153e-03
 -7.43932220e-02 -3.22219928e-01 -5.02656177e-02 -8.97978259e-02
  5.21966829e-02 -7.85785998e-02  1.03443968e-02  4.68965026e-02
 -2.01259572e-01 -7.57496400e-02  3.56489605e-02 -1.62831362e-02
 -6.61719763e-02 -6.93938274e-02  2.43822690e-01  5.72684658e-03
 -1.18857609e-01 -5.18812427e-03  6.30180334e-02  2.27280121e-01
  2.38319930e-01  2.24391399e-02  1.00741154e-02 -8.59901212e-02
  8.00377724e-02 -2.78762068e-01  1.76054747e-02  1.63331445e-01
  1.28117116e-01  5.09446000e-02  9.55198801e-02 -1.46233060e-01
 -5.87715414e-03  1.08365405e-01 -1.46253113e-01  3.84506953e-02
  3.71952591e-02 -7.58094405e-02 -4.17567407e-02 -6.21057401e-02
  1.35985226e-01  4.86549617e-02 -6.38772118e-02 -1.22995454e-01
  1.66152716e-01 -1.32430966e-01 -6.21145616e-02  2.96302935e-02
 -6.69127676e-02 -1.96030891e-01 -3.12722568e-01  1.85203480e-02
  3.22238571e-01  1.40385874e-01 -2.11475301e-01  6.55279486e-04
 -6.08998531e-02 -9.11745953e-02  4.87538214e-02  1.15339450e-02
 -8.66129840e-02 -1.15339318e-01 -9.13018480e-02  2.12021446e-02
  2.06243470e-01 -5.63902479e-02 -1.51062217e-02  1.96088861e-01
 -1.35765360e-02 -5.51577760e-02  2.70788466e-02  2.71301701e-02
 -1.04843079e-01 -6.85525124e-03 -1.31720495e-01 -6.98822616e-03
  7.44074771e-02 -1.03052152e-01 -1.64584187e-03  1.10587146e-01
 -1.91175313e-01  1.11058030e-01 -2.44834974e-02 -7.86092168e-02
 -8.42990351e-03 -9.05520684e-02 -9.67876883e-02  3.16291520e-02
  1.97211598e-01 -2.24565128e-01  2.27383363e-01  1.94193628e-01
 -3.77088829e-02  1.12419751e-01  5.70327681e-02  4.36559534e-02
 -6.87037407e-03  2.56834106e-02 -1.66926378e-01 -1.58188152e-01
  4.85156147e-02 -3.01366078e-04  1.58843200e-03  1.68875411e-02]
############################################################
```

### Images Failed

Some images of the dataset generate exceptions that can be caused by issues in the `face_recognition.face_encodings` or caused by `IndexError`. These exceptions will require some improvements to avoid these returns.

### Hardware Issues

Based on so limited hardware resources available to work on this challenge was some errors caused by unprocessed images. These cases are not connected with the code as the exceptions mentioned above. In a normal enterprise environment, these unprocessed cases will be reduced to zero.

## TODO/Bottlenecks

Some suggestions to improve the current solution:

- [ ] Create a better human interface to manage the whole process. (API, Swagger and Flask)
- [ ] Create a cluster to RabbitMQ service.
- [ ] Create a cluster to Producer service.
- [ ] Improve the control of Exceptions and use of hardware resource.
- [ ] Implementing the CI and gateways of software quality(pylint, pep8, pyflakes).
- [ ] Implementing the automation to build the new container images.
- [ ] Implementing the CD process to delivery automaticly the new releases generate on Git repository.
- [ ] Improve the limitations of resources in use by containers in general.
- [ ] Implement the configuration maps inside of Kubernetes.
- [ ] Add credentials to Secrets of Kubernetes or another KeyVault solution.
- [ ] Fix some issues in the face_recognition library that it's affecting some examples of images, generating exceptions and unexpected vectors.
- [ ] Learn more about numpy and face_recognition libraries to develop a better solutions.
