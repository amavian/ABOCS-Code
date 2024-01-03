@author: amavian

This document explains how to align the system, first by hand, and then with code.

We want the incoming beam to be well-collimated. I've been using the Thorlabs Wavefront Sensor to test the collimation using the RMS parameter and 
the 5th Zernike mode. Once we are happy that the beam is not expanding and the wavefront is flat, we can align the two steering mirrors. Ideally, these
steering mirrors will reflect the beam at 90-degree angles. This makes things easier. I often use a target grid to do near-far alignment, although this
isn't completely necessary. 

The collimating lens should not be chosen arbitrarily. It must have a similar beam waist diameter as the incoming beam. It must also be calibrated to 
the correct wavelength. This is a tedious process and involves adjusting 5 degrees of freedom. Again, it is helpful to use the Wavefront Sensor.

To couple the beam into the fiber, first, begin by using a 635 nm lens for backpropagation alignment. The better you do this step, the easier the subsequent
steps will be. To adjust the motorized steering mirrors, you can rotate the flexible coupler by hand as long as the power is off. When you’re happy with the
alignment, plug the output SMF fiber into the Thorlabs powermeter. If you’re using FC/APC fiber, make sure you are using the correct end! Hopefully, you will 
see at least microwatts of power, although this depends on the fundamental power. 

Now turn on the DC power supply for the Microstep drivers and ensure that the Raspberry Pi is on. Run the program motorControl.py. This allows you to adjust
the mirrors precisely and is meant to be used before the automatic alignment to attain initial coupling. This program allows you to type in commands (in the 
form "motor, stepSize") and it will make the corresponding adjustment. It will also print the power measurement, however, this is the power from the photodetector
which at this point will be off.

Motors 1 and 3 are vertical and motors 2 and 4 are horizontal. Using this program, you should quickly achieve coupling into the milliwatt regime. This, again,
depends on the fundamental power and how well you performed the backpropagation alignment. Once you're satisfied with the alignment, unplug the fiber from
the powermeter and plug it into the photodetector. Ensure that the photodetector is on and take a power reading of the beam before the collimating lens. Plug
this value into the code as the "fundamental" variable. You can now run fiberCoupler.py. As described in the file, for the initial optimization you should 
run the full walkBeam() function. This will take a few minutes but may not perform as well as intended. See the hardware section for troubleshooting.

The highest coupling I achieved was 80%. This was done through a time-consuming process of adjusting the 5 degrees of freedom on the fiber collimating lens.
After each adjustment, it was necessary to realign the system to check whether it improved or not. However, once the lens is well-calibrated, it should not be
adjusted.

At this point, hopefully, you are attaining good coupling. If you use randomScramble.py to perturbate the system out of alignment, you can quickly return the
coupling efficiency using the singleMotorOptimization() function in the fiberCoupler.py file. This will take less than a minute to converge, starting from as 
low as 1% efficiency.

The continuousOptimization() function in the fiberCoupler.py file will attempt to stabilize the power over long durations of time by making small adjustments,
looking for improvements in power. If it detects a "significant" drop in power, it will increase the step sizes and return to good coupling. In reality, I wrote
this function in about 20 minutes so I could get some nice-looking plots. While it does stabilize the power for short periods of time, after a few minutes the
power will slowly start to decrease. This can easily be improved upon but I lacked the time to do so.

Two limiting factors in this system are the noise floor and saturation limit of the photodetector. I did not look deeply into this so there is certainly 
room for improvement. The gain can be adjusted on the photodetector, however, as the saturation limit increases so does the noise floor. Changing the bias
voltage and load resistance could improve this.

In order to display accurate optical power measurements in the code, the conversion must be found between the raw photodetector output voltage and the
power measurement in milliwatts. This is different for each gain setting. To find the conversion, you can plot a known power with the raw photodetector reading
and find the best-fit equation. It is linear up until the saturation limit.
