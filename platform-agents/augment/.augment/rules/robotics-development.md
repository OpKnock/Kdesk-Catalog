---
type: agent_requested
description: "Develops ROS 2 systems: topics, nodes, launch files, parameter control, and rosbag recording/playback."
---

# robotics-development

Develops ROS 2 systems: topics, nodes, launch files, parameter control, and rosbag recording/playback.

## Instructions

# Robotics Development

Build and debug robot software with ROS 2.

## When to Use

- Robot perception, navigation, and control
- Simulated robot stacks (Gazebo)
- Logging and replay of robot runs

## Inspect the graph

```bash
ros2 topic list
ros2 node list
ros2 topic echo /odom --field linear.x
```

## Control and params

```bash
ros2 param set /turtlebot background_r 255
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist '{"linear": {"x": 0.1}}' --once
```

## Launch

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Launch files bring up nodes, params, and remappings together.

## Record and replay

```bash
ros2 bag record /odom /scan /cmd_vel -o nav_run1
ros2 bag info nav_run1
ros2 bag play nav_run1 --rate 0.5
```

Replays let you debug perception without hardware.

## Best practices

- Namespace topics by robot id for multi-robot.
- Use lifecycle nodes for deterministic startup.
- Record bags for every on-robot experiment.
- Simulate first; hardware time is precious.

## Testing

Run the stack in simulation, record a bag, replay, and compare metrics.

## Capabilities

### ros2-cli
Inspect and operate the ROS 2 graph.

**Commands:**
- `ros2 topic list`
- `ros2 topic echo /odom --field linear.x`
- `ros2 node list`
- `ros2 node info /turtlebot`
- `ros2 param set /turtlebot background_r 255`

**Examples:**
- ros2 topic info /cmd_vel -v
- ros2 topic echo /scan --once | head -20
- ros2 node list | grep -E 'nav|move'

### launch-bags
Launch systems and record/playback data.

**Commands:**
- `ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py`
- `ros2 bag record -a -o rosbag2_2026_08_10`
- `ros2 bag record /odom /scan /cmd_vel -o nav_run1`
- `ros2 bag play rosbag2_2026_08_10`
- `ros2 bag info rosbag2_2026_08_10`

**Examples:**
- ros2 bag record -a -o run_$(date +%F)
- ros2 bag play rosbag2_2026_08_10 --rate 0.5
- ros2 bag info rosbag2_2026_08_10 | head -20