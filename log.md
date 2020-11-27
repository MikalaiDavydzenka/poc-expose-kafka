after first installation

```yaml
    k8s-node-1:
      broker_id: '0'
      kafka_pod: kafka-0
    k8s-node-2:
      broker_id: '2'
      kafka_pod: kafka-2
    k8s-node-3:
      broker_id: '1'
      kafka_pod: kafka-1
```



k cp kafka-zookeeper-0:/bitnami/zookeeper/data/myid /tmp/zookeeper-0

    [k8s-node-1]
      broker_id     : 0
      kafka_pod     : kafka-0
  
      zookeeper_id  : 0
      zookeeper_pod : kafka-zookeeper-1
    [k8s-node-3]
      broker_id     : 1
      kafka_pod     : kafka-1
  
      zookeeper_id  : 2
      zookeeper_pod : kafka-zookeeper-2
    [k8s-node-2]
      broker_id     : 2
      kafka_pod     : kafka-2
  
      zookeeper_id  : 1
      zookeeper_pod : kafka-zookeeper-0



  msg: |-
    [k8s-node-1]
      broker_id     : 1001
      kafka_pod     : kafka-2
  
      zookeeper_id  : 1
      zookeeper_pod : kafka-zookeeper-0
    [k8s-node-3]
      broker_id     : 1003
      kafka_pod     : kafka-1
  
      zookeeper_id  : 3
      zookeeper_pod : kafka-zookeeper-2
    [k8s-node-2]
      broker_id     : 1002
      kafka_pod     : kafka-0
  
      zookeeper_id  : 2
      zookeeper_pod : kafka-zookeeper-1