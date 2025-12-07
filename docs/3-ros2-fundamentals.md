---
sidebar_label: 'ROS 2 Fundamentals'
sidebar_position: 4
---

# ROS 2 Fundamentals

## Introduction to ROS 2

This chapter introduces ROS 2 installation and setup, nodes, topics, services, and basic robot control and simulation. ROS 2 (Robot Operating System 2) provides a collection of tools, libraries, and conventions for building robot applications. Nodes are processes that perform computation, topics are named buses over which nodes exchange messages, and services allow nodes to send requests and receive responses.

## ROS 2 Architecture

ROS 2 is built around three fundamental communication concepts: nodes, topics, and services. Nodes are the basic computational elements that perform specific functions. Topics allow nodes to publish and subscribe to streams of data. Services enable request-response communication between nodes, allowing one node to request specific actions from another.

### Nodes

Nodes are the basic computational elements that perform specific functions. In ROS 2, nodes are implemented as processes that communicate with each other using a pub/sub messaging model. Each node runs a specific task such as sensor processing, motion control, or perception.

### Topics

Topics allow nodes to publish and subscribe to streams of data. They enable asynchronous communication between nodes where publishers send messages to a topic and subscribers receive messages from that topic. Topics are ideal for streaming data like sensor readings or robot state.

### Services

Services enable request-response communication between nodes, allowing one node to request specific actions from another. Unlike topics, services provide synchronous communication where the requesting node waits for a response from the service provider.

## Key Features of ROS 2

ROS 2 offers several improvements over ROS 1:

- **Real-time support**: Better real-time performance for critical applications
- **Multi-robot systems**: Improved support for multi-robot coordination
- **Security**: Built-in security features for safe robot operation
- **DDS Integration**: Uses Data Distribution Service for communication
- **Quality of Service (QoS)**: Configurable communication reliability

## ROS 2 Programming

ROS 2 supports multiple programming languages with Python and C++ being the most common. The core concepts remain consistent across languages:

- Node creation and lifecycle management
- Publisher and subscriber implementation
- Service and action client/server patterns
- Parameter management and configuration

## Installation and Setup

ROS 2 installation varies by distribution (Humble Hawksbill, Iron Irwini, Jazzy Jalisco). The installation process includes:

1. Setting up the apt repository
2. Installing ROS 2 packages
3. Sourcing the ROS 2 environment
4. Verifying the installation with basic examples

## Basic Robot Control

ROS 2 provides standardized interfaces for robot control:

- **Joint State Messages**: Publishing current joint positions
- **Joint Trajectory Actions**: Controlling joint movements
- **Twist Messages**: Controlling robot base movement
- **TF Transforms**: Managing coordinate frames

### Code Snippets

```python
# Placeholder for runnable Python code snippet 1
# Example: Basic ROS 2 publisher node
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

# Placeholder for runnable Python code snippet 2
# Example: Basic ROS 2 subscriber node
class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

# Placeholder for runnable Python code snippet 3
# Example: ROS 2 service client
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class MinimalClientAsync(Node):
    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        return self.cli.call_async(self.req)
```

### Exercises

1.  Create a ROS 2 node that publishes joint state messages for a simple robot
2.  Implement a service that controls a robot's movement based on distance and direction parameters