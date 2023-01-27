from setuptools import setup, find_packages
import os

from easy_dc.graph import make_dcgraph
from easy_dc.utils import uon


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPH_DIR = os.path.join(ROOT_DIR, 'data', 'graphs')


def create_graph_folder():
    if not os.path.exists(GRAPH_DIR):
        os.makedirs(GRAPH_DIR)


def post_install():
    create_graph_folder()
    for order in uon(32, 26208):
        make_dcgraph(order)


setup(
    name='easy_dc',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'easy_dc = easy_dc.__main__:main',
            'easy_dc-solve=easy_dc.weave:weave_discocube'
        ]
    },
    zip_safe=False,
    cmdclass={
        'post_install': post_install
    }
)
