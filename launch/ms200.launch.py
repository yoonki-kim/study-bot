import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

def generate_launch_description():

    package_name = 'study-bot'

    # 1. 런치 인자 선언 (동적 포트 할당 및 시뮬레이션 시간 설정)
    use_sim_time = LaunchConfiguration('use_sim_time')
    port_name = LaunchConfiguration('port_name')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use sim time if true')

    declare_port_name = DeclareLaunchArgument(
        'port_name',
        default_value='/dev/ttyUSB0',
        description='LIDAR port name')

    # 2. robot_state_publisher 실행 (study-bot 패키지의 rsp.launch.py 포함)
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
        )]), launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # 3. MS200 LiDAR 퍼블리셔 노드 설정
    # 노드 이름: ms200_lidar_noe
    # 파라미터: 단일 딕셔너리로 선언
    ms200_lidar_node = Node(
        package='oradar_lidar',
        executable='oradar_scan',
        name='ms200_lidar_noe',
        output='screen',
        parameters=[{
            'device_model': 'MS200',
            'frame_id': 'laser_frame',
            'scan_topic': '/scan',
            'port_name': port_name,
            'baudrate': 230400,
            'angle_min': 0.0,
            'angle_max': 360.0,
            'range_min': 0.05,
            'range_max': 20.0,
            'clockwise': False,
            'motor_speed': 10
        }]
    )

    # 모든 액션 반환
    return LaunchDescription([
        declare_use_sim_time,
        declare_port_name,
        rsp,
        ms200_lidar_node
    ])
