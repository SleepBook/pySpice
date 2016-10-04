Project Introduction
===================================

Welcome! This project realizes a SPICE compatible circuit simulator in Python. Current the simulator supports DC Sweep, AC and Transient analysis of the circuits with various electronic devices. These devices include:

	+ Resistor
	+ Capacitor
	+ Inductor
	+ Voltage Controlled Voltage Source (VCVS)
	+ Voltage Controlled Current Source (VCCS)
	+ Current Controlled Voltage Source (CCVS)
	+ Current Controlled Current Source (CCCS)
	+ Diode (only support basic model)
	+ MOSFET (PMOS and NMOS, only basic model)
	+ Voltage/Current Source (With Time-Variant Transient Stimulates Support: Including Waveform of Sinusoidal, Staircase, Adjustable Pulse)

For a quick start, please refer to the `Tutorial & Installation <usage.html>`_ section. It will guide you to install this program and run several samples.

If you are unfamiliar with the knowledge of electronic circuit and circuit simulation, you may find this `book <book.html>`_ very helpful, where I introduce the theory and algorithm in detail.

If you are also a novice programmer like me, you may well want to read some chapters of the book mentioned above. There I introduce the structure of this project and the design considerations behind it. This is the most difficult part I found in building this project, to design the structure of the project and the APIs of each module. Of course, any advices are MUCH welcomed, I believe I can learn a lot from your advices :)

This is the first 'real' software project of mine. I invested considerable time and efforts in its decelopment, trying to make it complete and friendly to anyone who is interested in it. At the same time, I know it’s far from perfect. That’s why I want to maintain it as a long-term project, so that I can receive your advices and continue to contribute to it and make it better and better. Also, I am looking forward to cooperation on developing and maintaining this project, too.

