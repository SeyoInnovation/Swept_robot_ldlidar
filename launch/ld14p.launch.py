#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
'''
参数描述：
---
- 设置激光扫描方向：
  1. 设置逆时针，例如：{'laser_scan_dir': True}
  2. 设置顺时针，例如：{'laser_scan_dir': False}
- 角度裁剪设置，在设置的角度范围内屏蔽数据：
  1. 启用角度裁剪功能：
    1.1. 启用角度裁剪，例如：{'enable_angle_crop_func': True}
    1.2. 禁用角度裁剪，例如：{'enable_angle_crop_func': False}
  2. 角度裁剪区间设置：
  - 在设置的角度范围内的距离和强度数据将被设置为 0。
  - 角度 >= 'angle_crop_min' 且角度 <= 'angle_crop_max'，即 [angle_crop_min, angle_crop_max]，单位为度。
    示例：
      {'angle_crop_min': 135.0}
      {'angle_crop_max': 225.0}
      即 [135.0, 225.0]，角度单位为度。
'''
def generate_launch_description():
  # LDROBOT 激光雷达发布节点
  ldlidar_node = Node(
      package='ldlidar',
      executable='ldlidar',
      name='ldlidar_publisher_ld14p',
      output='screen',
      parameters=[
        {'product_name': 'LDLiDAR_LD14P'},
        {'topic_name': 'scan'},
        {'port_name': '/dev/ttyACM0'}, # 串口
        {'frame_id': 'base_laser'},
        {'laser_scan_dir': True},
        {'enable_angle_crop_func': False},#单角度裁剪开关：值为False时表示不使用多角度裁剪，默认为False
        {'angle_crop_min': 135.0},#单角度裁剪开始值
        {'angle_crop_max': 225.0},#单角度裁剪结束值
        {'truncated_mode_': 0}#值为1表示使用多角度裁剪，同时enable_angle_crop_func设为False，角度值在/main.cpp中修改
      ]
  )
  # base_link 到 base_laser 的 TF 节点
  base_link_to_laser_tf_node = Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    name='base_link_to_base_laser_ld14p',
    arguments=['0','0','0.18','0','0','0','base_link','base_laser']
  )
  scan_fre_node = ExecuteProcess(
    cmd=['ros2','run','ldlidar','LD14P_scan_fre.py']
  )
  # 定义 LaunchDescription 变量
  ld = LaunchDescription()
  #ld.add_action(scan_fre_node) #<!--调节雷达扫描频率，scan_fre扫描频率与雷达串口号请在LD14P_scan_fre.py文件中修改-->
  ld.add_action(ldlidar_node)
  ld.add_action(base_link_to_laser_tf_node)
  return ld