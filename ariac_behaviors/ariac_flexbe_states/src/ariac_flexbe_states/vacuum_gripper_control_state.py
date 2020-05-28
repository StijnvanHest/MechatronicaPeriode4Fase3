#!/usr/bin/env python
import rospy
import sys
import rostopic
from flexbe_core import EventState
from osrf_gear.srv import VacuumGripperControl, VacuumGripperControlRequest, VacuumGripperControlResponse
from osrf_gear.msg import VacuumGripperState
from std_msgs.msg import String

class VacuumGripperControlState(EventState):
	'''
	Example for a state to demonstrate which functionality is available for state implementation.
	This example lets the behavior wait until the given target_time has passed since the behavior has been started.

	-- enable 	bool 	New state of the gripper.

	#> arm_id	string	Arm identifier

	<= continue 		Action succeeded.
	<= failed 		Action failed.
	<= invalid_arm_id	Invalid arm id

	'''

	def __init__(self, enable):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(VacuumGripperControlState, self).__init__(input_keys = ['arm_id'], outcomes = ['continue', 'failed', 'invalid_arm_id'])

		# Store state parameter for later use.
		self._enable = enable

		pass # Nothing to do in this example.


	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.

		if userdata.arm_id == 'right_arm':
			gripper_service = '/ariac/right_arm/gripper/control'
		else:
			if userdata.arm_id == 'left_arm':
				gripper_service = '/ariac/left_arm/gripper/control'
			else:
				return 'invalid_arm_id'

	    	rospy.loginfo("Waiting for service...")
	    	rospy.wait_for_service(gripper_service) # use arm2 for controlling gripper on second manipulator
	    	try:
			# Create a service proxy.
			vacuum_gripper_control = rospy.ServiceProxy(gripper_service, VacuumGripperControl)


			request = VacuumGripperControlRequest()
			request.enable = self._enable

			# Call the service here.
			service_response = vacuum_gripper_control(request)

			rospy.loginfo("I only got here AFTER the service call was completed!")

			# Return the response to the calling function.
			if service_response.success == True:
				if self._enable == True:
					if userdata.arm_id == 'right_arm':
						status = rospy.wait_for_message('/ariac/right_arm/gripper/state', VacuumGripperState)
						if status.attached == True:
							return 'continue'
					elif userdata.arm_id == 'left_arm':
						status = rospy.wait_for_message('/ariac/left_arm/gripper/state', VacuumGripperState)
						if status.attached == True:
							return 'continue'
					else:
						return 'failed'
				else:
					return 'continue'
			else:
				return 'failed'

	    	except rospy.ServiceException, e:
			rospy.loginfo("Service call failed: %s"%e)
			return 'failed'


		pass # Nothing to do in this example.
		

	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
		# It is primarily used to start actions which are associated with this state.

		# The following code is just for illustrating how the behavior logger works.
		# Text logged by the behavior logger is sent to the operator and displayed in the GUI.
		
		pass
       		''' time_to_wait = (self._target_time - (rospy.Time.now() - self._start_time)).to_sec()
        	if time_to_wait > 0:
            		Logger.loginfo('Need to wait for %.1f seconds.' % time_to_wait) '''


	def on_exit(self, userdata):
		# This method is called when an outcome is returned and another state gets active.
		# It can be used to stop possibly running processes started by on_enter.
		pass # Nothing to do in this example.


	def on_start(self):
		# This method is called when the behavior is started.
		# If possible, it is generally better to initialize used resources in the constructor
		# because if anything failed, the behavior would not even be started.

		# In this example, we use this event to set the correct start time.
		self._start_time = rospy.Time.now()


	def on_stop(self):
		# This method is called whenever the behavior stops execution, also if it is cancelled.
		# Use this event to clean up things like claimed resources.
		pass # Nothing to do in this example.
		
