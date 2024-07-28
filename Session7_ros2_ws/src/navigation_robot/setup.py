from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'navigation_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name,'launch'),glob('launch/*.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mohamad',
    maintainer_email='mohamadnasser.engr@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'wall_finder=navigation_robot.wall_finder_service:main',
            'robot_driver=navigation_robot.robot_driver:main',
            'lap_time_server=navigation_robot.lap_time_server:main',
            'lap_time_client=navigation_robot.lap_time_client:main'
        ],
    },
)
