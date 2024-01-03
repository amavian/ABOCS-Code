@author: amavian

Automatic Beam Output Coupling System (ABOCS) Code is a compilation of code and instructions for whoever takes on the challenge of continuing this 
project of developing a cost-effective stepper motor controlled motorized steering mirror system capable of achieving high-efficiency fiber coupling and power
stabilization. This work was done in the fall of 2023 in the Instrumentation Division at Brookhaven National Laboratory.

In the process of editing this code to neaten it up, I have made some considerable changes (without testing), which at best will cause some inconsistent tab
errors and at worst may result in some more serious syntax errors. I have also renamed files so a table below will provide you with their original names (which 
are their current names on the FSL Raspberry Pi in Lab 4).

Many of these changes are to enhance readability, provide clarity, or standardize my coding style. In addition, I made many comments to describe the programs and
functions. However, in my review, I also found some errors in my logic. For example, while the goal of my project was to realize remote automatic alignment, I
only tested the remote feedback once. It was late on a Friday night. I was able to see in real-time the changing power downstairs as I adjusted the positions of 
the motors, but when I ran my fiberCouplerRemote.py code, it did not converge. I assumed it was an easy fix, but I never connected the fiber again to troubleshoot. 
The error had to do with a change I made to the moveBy() function and resulted in the program only allowing the motors to move in one direction. 

In my writing, I refer to the functions without including the parameters for the ease of the reader. For full descriptions of the functions, see the files 
themselves.

This entire folder is split into two sub-folders: "Stepper Motors" and "Piezo Linear Actuators". Unless you are interested in working with the piezo actuators 
again, you can ignore that folder. Within the "Stepper Motors" folder are two additional folders, titled "Local Feedback" and "Remote Feedback." Local feedback
refers to using the photodetector in Lab 4 as feedback to the steering mirror system, in contrast to the remote photodetector in the basement.

Within the "Mavian ABOCS Code" folder, there are three instruction text files that describe how to implement the code. 

- FIBER COUPLING INSTRUCTIONS
- NETWORK CONNECTION INSTRUCTIONS
- SERVO INSTRUCTIONS


HARDWARE:

The idea to use stepper motors came very early on in the semester, but it wasn't until November that we began working on it. This was an attempt to escape the
hysteresis problem that existed in the piezoelectric actuators. The lack of reproducibility in the servos was a limiting factor in the algorithms that could be
implemented. Tests can be done to measure the hysteresis in a given fiber coupling system as described in my paper. From what I found, the stepper motors performed
better than the servos, but both suffered from hysteresis. This already is very good considering the piezo linear actuators cost $771 per servo, compared to
$11 per stepper motor.

In general, hysteresis is worse when the step sizes are larger. The stepper motors displayed this behavior, but in addition, they occasionally skipped steps or 
stalled completely. To design an improved ABOCS, the hardware must be optimized before the software can be optimized. Here are some ideas to test:

- Increase the holding torque of the motors
- Reduce friction in motor-mirror coupler
- Optimize the drive signal to the motors 
- Increase the power/current to the Microstep drivers
- Use a different commercial mirror stage

The wiring of the Raspberry Pi, Microstep drivers, and stepper motors is an area for improvement. It would also be helpful to have a plate to attach all the 
drivers to. I attached a link in the "HELPFUL LINKS" section that describes how to wire the system.


SOFTWARE:

If the hardware is perfected, much more interesting and elegant solutions can be implemented that will perform much stronger under unideal conditions. My current
algorithm, as I will discuss in further detail later, uses a modified gradient descent method. I refer to it as a gradient descent algorithm as it attempts to 
minimize the loss of power and the parameters iteratively move in the opposite direction of the gradient. However, it is not the same as a machine learning
algorithm in that it does not calculate the actual gradient and the objective function is based on real-world data, not a mathematical function.

Nonetheless, this search method can only be expected to find the global maximum for monotonic point spread functions. Even in the best case of Adaptive Optics
performance, Fresnel diffraction invokes a Bessel function in the case of a circular aperture which reduces the algorithm’s effectiveness. Future incarnations 
should incorporate a non-deterministic search method, such as a Stochastic Parrallel Gradient Descent (SPDG) algorithm.


HELPFUL LINKS:

https://pi-plates.com/daqc2-users-guide/
https://www.instructables.com/Raspberry-Pi-Python-and-a-TB6600-Stepper-Motor-Dri/

Optical Fiber 101: Understanding Single Mode Fiber (Part 1 of 2)
https://youtu.be/FbOXRuBQt_U?si=dKXPgCyG_2KjBVFu

Optical Fiber 101: Using Single Mode Fiber (Part 2 of 2)
https://youtu.be/HvJeXakc8Kc?si=AHeF4uTbCcpt43XE


TABLE:

Edited Name => Original Name
fiberCoupler.py => fiberCoupler.py
motorControl.py => motorControl2.py
photodetectorTest.py => PhotodiodeTest.py
randomScramble.py => RandomScramble.py
clientCode.py => clientCode2.py
fiberCouplerRemote.py => fiberCouplerRemote.py
motorControlRemote.py => motorControl3.py
serverCode.py => serverCode3.py (on the downstairs Pi)
newport.py => newport.py
servoFiberCoupler.py => FiberCoupler1.py


ACKNOWLEDGMENTS:

Special thanks to Samuel Woronick, Rishikesh Gokhale, Justine Haupt, and Julian Martinez-Rincon.
