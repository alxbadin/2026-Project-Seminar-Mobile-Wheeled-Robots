from launch import LaunchDescription
from launch.actions import (
    ExecuteProcess,
    TimerAction,
    LogInfo,
    RegisterEventHandler,
)
from launch_ros.actions import Node
from launch.event_handlers import OnProcessStart


def generate_launch_description():

    turtlesim = Node(
        package="turtlesim", executable="turtlesim_node", name="turtlesim"
    )

    kill_turtle = ExecuteProcess(
        cmd=[
            "ros2",
            "service",
            "call",
            "/kill",
            "turtlesim/srv/Kill",
            "{name: turtle1}",
        ],
        output="screen",
    )

    spawn_zero = ExecuteProcess(
        cmd=[
            "ros2",
            "service",
            "call",
            "/spawn",
            "turtlesim/srv/Spawn",
            "{x: 1.5, y: 2.0, theta: 0.0, name: 'zero'}",
        ],
        output="screen",
    )

    spawn_one = ExecuteProcess(
        cmd=[
            "ros2",
            "service",
            "call",
            "/spawn",
            "turtlesim/srv/Spawn",
            "{x: 7.0, y: 2.0, theta: 1.5708, name: 'one'}",
        ],
        output="screen",
    )

    zero = Node(
        package="practice_turtlesim",
        executable="digit_drawer",
        name="draw_zero",
        parameters=[
            {"turtle": "zero"},
            {"digit": "0"},
        ],
        output="screen",
    )

    one = Node(
        package="practice_turtlesim",
        executable="digit_drawer",
        name="draw_one",
        parameters=[
            {"turtle": "one"},
            {"digit": "1"},
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            turtlesim,
            RegisterEventHandler(
                OnProcessStart(
                    target_action=turtlesim,
                    on_start=[
                        LogInfo(msg="Turtlesim started, spawning turtles"),
                        kill_turtle,
                        spawn_zero,
                        spawn_one,
                    ],
                )
            ),
            TimerAction(period=1.0, actions=[zero, one]),
        ]
    )
