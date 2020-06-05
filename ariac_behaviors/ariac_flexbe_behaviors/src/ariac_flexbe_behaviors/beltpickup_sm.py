#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from flexbe_states.wait_state import WaitState
from ariac_support_flexbe_states.replace_state import ReplaceState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri May 29 2020
@author: Stijn van Hest
'''
class BeltPickUPSM(Behavior):
	'''
	This is a behaivor that picks a part of the belt
	'''


	def __init__(self):
		super(BeltPickUPSM, self).__init__()
		self.name = 'BeltPickUP'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1374 y:114, x:1202 y:412
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['ARMidMAIN', 'PartPose', 'PartOffset', 'exactparttype', 'PartTYPE'], output_keys=['RightArmItem', 'LeftArmItem'])
		_state_machine.userdata.ARMidMAIN = ''
		_state_machine.userdata.arm_idR = 'right_arm'
		_state_machine.userdata.move_groupR = 'Right_Arm'
		_state_machine.userdata.move_groupL = 'Left_Arm'
		_state_machine.userdata.tool_linkR = 'right_ee_link'
		_state_machine.userdata.tool_linkL = 'left_ee_link'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.PartOffset = 0
		_state_machine.userdata.PartPose = []
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.arm_idL = 'left_arm'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.exactparttype = ''
		_state_machine.userdata.RightArmItem = ''
		_state_machine.userdata.LeftArmItem = ''
		_state_machine.userdata.PartTYPE = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:232 y:59
			OperatableStateMachine.add('UseRightArm?',
										EqualState(),
										transitions={'true': 'ComputeBeltPickForRightArm', 'false': 'ComputeBeltPickForLeftArm'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'ARMidMAIN', 'value_b': 'arm_idR'})

			# x:484 y:63
			OperatableStateMachine.add('ComputeBeltPickForRightArm',
										ComputeGraspAriacState(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'GoToPickRight', 'failed': 'WaitFailed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupR', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_linkR', 'pose': 'PartPose', 'offset': 'PartOffset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:484 y:155
			OperatableStateMachine.add('ComputeBeltPickForLeftArm',
										ComputeGraspAriacState(joint_names=['left_shoulder_pan_joint', 'left_shoulder_lift_joint', 'left_elbow_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'GoToPickLeft', 'failed': 'WaitFailed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupL', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_linkL', 'pose': 'PartPose', 'offset': 'PartOffset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:701 y:57
			OperatableStateMachine.add('GoToPickRight',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'TurnGripperONRight', 'planning_failed': 'TurnGripperONRight', 'control_failed': 'TurnGripperONRight'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupR', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:701 y:164
			OperatableStateMachine.add('GoToPickLeft',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'TurnGripperONLeft', 'planning_failed': 'TurnGripperONLeft', 'control_failed': 'TurnGripperONLeft'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupL', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:874 y:58
			OperatableStateMachine.add('TurnGripperONRight',
										VacuumGripperControlState(enable=True),
										transitions={'continue': 'SetRightArmItem', 'failed': 'ComputeBeltPickForRightArm', 'invalid_arm_id': 'WaitFailed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idR'})

			# x:874 y:165
			OperatableStateMachine.add('TurnGripperONLeft',
										VacuumGripperControlState(enable=True),
										transitions={'continue': 'SetLeftArmItem', 'failed': 'ComputeBeltPickForLeftArm', 'invalid_arm_id': 'WaitFailed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idL'})

			# x:848 y:478
			OperatableStateMachine.add('WaitFailed',
										WaitState(wait_time=2),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:1045 y:58
			OperatableStateMachine.add('SetRightArmItem',
										ReplaceState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'PartTYPE', 'result': 'RightArmItem'})

			# x:1041 y:163
			OperatableStateMachine.add('SetLeftArmItem',
										ReplaceState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'PartTYPE', 'result': 'LeftArmItem'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
