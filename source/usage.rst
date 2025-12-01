Usage
=====
Acknowledgements
----------------

LHMP is being developed in collaboration with NASA Langley Research Center and the Hampton University.


Copyright
---------

.. include:: ../LICENSE


Configuring the Raspberry Pi
----------------------------

This section summarizes the steps required to setup the environment needed to run a GigE Vision (i.e., genicam) camera on a Raspberry Pi 4b. Here we use a Pheonix 5.0 Polarization camera (LUCID Vision Labs Inc., 2023) that is built around Sony's IMX250MYR CMOS.

Hardware Requirements
	1) Any GigE vision camera should work however it must be a GenICam compliant machine vision camera/device. 
		a) Power supply.
	
	2) Rasberry Pi 4b running Debian GNU/Linux 12 (bookworm) x64. Prefer remote connection with Raspberry Pi Connect. 
		a) Power supply.
	
	3) Ethernet Cable.

Setup Hardware
	a) Connect camera to Raspberry Pi via ethernet cable.

	b) Power Raspberry Pi.

Install ArenaSDK Software (ArenaSDK_v0.1.78_Linux_ARM64)
	.. note::

		Full details in 'README_ARM64.txt'


	a) Set jumbo frames
		.. code-block:: console

			$ sudo ip link set enp0s8 mtu 9000

	b) Set receive buffers
		.. code-block:: console

			$ sudo ethtool -g enp0s8
			$ sudo ethtool -G enp0s8 rx 4096

	c) Set socket buffer size
		.. code-block:: console

			$ sudo sh -c "echo 'net.core.rmem_default=33554432' >> /etc/sysctl.conf"
			$ sudo sh -c "echo 'net.core.rmem_max=33554432' >> /etc/sysctl.conf"
			$ sudo sysctl -p
		
	d) Reverse path filtering
		.. code-block:: console

			$ sudo sh -c "echo 'net.core.rmem_default=33554432' >> /etc/sysctl.conf"
			$ sudo sh -c "echo 'net.core.rmem_max=33554432' >> /etc/sysctl.conf"
			$ sudo sysctl -p

	e) Extract the tarball to your desired location:	
		.. code-block:: console

	   		$ tar -xvzf ArenaSDK_Linux_ARM64.tar.gz
	    
	f) Run the ArenaSDK_Linux_ARM64.conf file	
		.. code-block:: console

	   		$ cd ~/Documents/ArenaSDK_v0.1.78_Linux_ARM64/ArenaSDK_Linux_ARM64
	   		$ sudo sh Arena_SDK_ARM64.conf


Install arena api
	a) Setup virtual environment.
		.. code-block:: console
	
			$ python3 -m venv myvirtualenv

	b) Activate virtual environment.
		.. code-block:: console
	
			$ source ~/myvirtualenv/bin/activate

	c) Install Harvesters.
		.. code-block:: console

			$ cd arena_api-2.7.1-py3-none-any
			$ pip install arena_api-2.7.1-py3-none-any.whl
			$ pip install -r examples/requirements_lin_arm64.txt
			$ sudo apt-get install python3-tk

	d) Install standard openCV.
		.. code-block:: console
	
			$ pip install opencv-python

			

Example of running programs in Arena api
-----------------------------------------
	a) Activate virtual environment.
		.. code-block:: console
	
			$ source ~/myvirtualenv/bin/activate

	b) Set appropriate directory with python scripts.
		.. code-block:: console
	
			$ cd ~/Documents/arena_api-2.7.1-py3-none-any/examples

	c) Run desired python script.
		.. code-block:: console
	
			$ python3 py_save.py


Instructions for building sphinx documentation locally
------------------------------------------------------

This section describes how to build the sphinx documentation locally. 


	a) Activate virtual environment.
		.. code-block:: console

			$ source ~/myvirtualenv/bin/activate


	b) Install matplotlib.
		.. code-block:: console

			$ pip install matplotlib

	c) Install basic sphinx package.
		.. code-block:: console

			$ pip install sphinx

	d) Install html theme for sphinx.
		.. code-block:: console

			$ pip install sphinx_rtd_theme

	e) Install pdf builder for sphinx.
		.. code-block:: console

			$ pip install sphinx-simplepdf

	f) Build sphinx.
		.. code-block:: console

			$ sphinx-build -b html source docs

Test the instrument functionality 
---------------------------------

.. autofunction:: TestSample.Run

Basic function for capturing samples with the LHMP
--------------------------------------------------

.. autofunction:: CaptureSample.Run

