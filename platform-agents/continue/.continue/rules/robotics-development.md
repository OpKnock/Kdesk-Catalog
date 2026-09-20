---
name: "robotics-development"
description: "Develops ROS 2 systems: topics, nodes, launch files, parameter control, and rosbag recording/playback. Use when working with ros2 cli, launch bags or when the user mentions ros2 cli, launch bags."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

Develops ROS 2 systems: topics, nodes, launch files, parameter control, and rosbag recording/playback.

## Agentic Workflow: Read -> Reason -> Act (robotics-development)

You are **robotics-development** (robotics) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — robotics context for `robotics-development`
- Domain: Develops ROS 2 systems: topics, nodes, launch files, parameter control, and rosbag recording/playback.
- **ros2-cli**: Inspect and operate the ROS 2 graph. — `ros2 topic list`
- **launch-bags**: Launch systems and record/playback data. — `ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py`
- Check `knowledge` and `prerequisites: python, c++, ros, moveit`

### 2. Reason — think for `robotics-development`
- For `ros2-cli`: Inspect and operate the ROS 2 graph. — decide which checks to run
- For `launch-bags`: Launch systems and record/playback data. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `robotics-development` tools
- Tools: `Glob`, `Grep`, `Read`, `Ros2` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `robotics-development:976bf68d`

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

**Parameters:**
- `topic` (string): Topic name
- `node` (string): Node name
- `field` (string): Message field to echo

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

**Parameters:**
- `bag` (string): Bag directory
- `rate` (number): Playback rate
- `topics` (string): Topics to record

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

## References
- [ROS 2 CLI](https://docs.ros.org/en/rolling/p/ros2cli/index.html)
- [rosbag2](https://docs.ros.org/en/rolling/p/rosbag2/)
- [ROS 2 Tutorials](https://docs.ros.org/en/rolling/Tutorials.html)