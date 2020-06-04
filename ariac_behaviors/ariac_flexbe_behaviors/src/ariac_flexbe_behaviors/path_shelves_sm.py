#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 28 2020
@author: Anne van Oirschot
'''
class Path_ShelvesSM(Behavior):
	'''
	Pakken van het part uit de shelves om te verplaatsen in op de AGV
	'''


	def __init__(self):
		super(Path_ShelvesSM, self).__init__()
		self.name = 'Path_Shelves'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1567 y:662, x:898 y:340
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['bin_id', 'camera_topic', 'camera_frame', 'part_type', 'PreGraspGantry', 'offset'])
		_state_machine.userdata.bin_id = ''
		_state_machine.userdata.home_gantry_id = 'Gantry_Home'
		_state_machine.userdata.home_rightarm_id = 'Right_PreGrasp'
		_state_machine.userdata.home_leftarm_id = 'Left_PreGrasp'
		_state_machine.userdata.move_group_right = 'Right_Arm'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.move_group_left = 'Left_Arm'
		_state_machine.userdata.move_group_gantry = 'Gantry'
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.PreGraspGantry = ''
		_state_machine.userdata.SafePosition = 'Gantry_ShelfSAFE'
		_state_machine.userdata.tool_link = 'right_ee_link'
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.offset = ''
		_state_machine.userdata.arm_id = 'right_arm'
		_state_machine.userdata.PreGrasp_RightArm = 'Right_Shelf'
		_state_machine.userdata.PreGrasp_LeftArm = 'Left_Shelf'
		_state_machine.userdata.SafePositionConveyor = 'Gantry_Shelf_Conveyor'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:37 y:112
			OperatableStateMachine.add('HomepositieRightArm',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'HomepositieLeftArm', 'planning_failed': 'Retry_1', 'control_failed': 'Retry_1', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home_rightarm_id', 'move_group': 'move_group_right', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:219 y:111
			OperatableStateMachine.add('HomepositieLeftArm',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'DetectPart', 'planning_failed': 'Retry_2', 'control_failed': 'Retry_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home_leftarm_id', 'move_group': 'move_group_left', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:62 y:33
			OperatableStateMachine.add('Retry_1',
										WaitState(wait_time=3),
										transitions={'done': 'HomepositieRightArm'},
										autonomy={'done': Autonomy.Off})

			# x:239 y:31
			OperatableStateMachine.add('Retry_2',
										WaitState(wait_time=3),
										transitions={'done': 'HomepositieLeftArm'},
										autonomy={'done': Autonomy.Off})

			# x:389 y:115
			OperatableStateMachine.add('DetectPart',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'SafePosition_Conveyor', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'part_pose'})

			# x:1279 y:116
			OperatableStateMachine.add('PreGraspGantry',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ComputePick', 'planning_failed': 'Retry_6', 'control_failed': 'Retry_6', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'PreGraspGantry', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1304 y:30
			OperatableStateMachine.add('Retry_6',
										WaitState(wait_time=3),
										transitions={'done': 'PreGraspGantry'},
										autonomy={'done': Autonomy.Off})

			# x:736 y:114
			OperatableStateMachine.add('SafePosition',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'PreGrasp_RightArm', 'planning_failed': 'Retry_3', 'control_failed': 'Retry_3', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'SafePosition', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:763 y:21
			OperatableStateMachine.add('Retry_3',
										WaitState(wait_time=3),
										transitions={'done': 'SafePosition'},
										autonomy={'done': Autonomy.Off})

			# x:1463 y:117
			OperatableStateMachine.add('ComputePick',
										ComputeGraspAriacState(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'MoveToPick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_right', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'part_pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1645 y:117
			OperatableStateMachine.add('MoveToPick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GripperOn', 'planning_failed': 'Retry_7', 'control_failed': 'GripperOn'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group_right', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1679 y:35
			OperatableStateMachine.add('Retry_7',
										WaitState(wait_time=3),
										transitions={'done': 'MoveToPick'},
										autonomy={'done': Autonomy.Off})

			# x:1465 y:242
			OperatableStateMachine.add('GripperOn',
										VacuumGripperControlState(enable=True),
										transitions={'continue': 'PreGraspRightArm', 'failed': 'ComputePick', 'invalid_arm_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:1480 y:333
			OperatableStateMachine.add('PreGraspRightArm',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'SafePosition_2', 'planning_failed': 'Retry_8', 'control_failed': 'Retry_8', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'PreGrasp_RightArm', 'move_group': 'move_group_right', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1697 y:328
			OperatableStateMachine.add('Retry_8',
										WaitState(wait_time=3),
										transitions={'done': 'PreGraspRightArm'},
										autonomy={'done': Autonomy.Off})

			# x:1479 y:426
			OperatableStateMachine.add('SafePosition_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'SafePosition_Conveyor_2', 'planning_failed': 'Retry_9', 'control_failed': 'Retry_9', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'SafePosition', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1700 y:427
			OperatableStateMachine.add('Retry_9',
										WaitState(wait_time=3),
										transitions={'done': 'SafePosition_2'},
										autonomy={'done': Autonomy.Off})

			# x:924 y:115
			OperatableStateMachine.add('PreGrasp_RightArm',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'PreGrasp_LeftArm', 'planning_failed': 'Retry_4', 'control_failed': 'Retry_4', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'PreGrasp_RightArm', 'move_group': 'move_group_right', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1103 y:113
			OperatableStateMachine.add('PreGrasp_LeftArm',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'PreGraspGantry', 'planning_failed': 'Retry_5', 'control_failed': 'Retry_5', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'PreGrasp_LeftArm', 'move_group': 'move_group_left', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:948 y:23
			OperatableStateMachine.add('Retry_4',
										WaitState(wait_time=3),
										transitions={'done': 'PreGrasp_RightArm'},
										autonomy={'done': Autonomy.Off})

			# x:1126 y:21
			OperatableStateMachine.add('Retry_5',
										WaitState(wait_time=3),
										transitions={'done': 'PreGrasp_LeftArm'},
										autonomy={'done': Autonomy.Off})

			# x:583 y:115
			OperatableStateMachine.add('SafePosition_Conveyor',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'SafePosition', 'planning_failed': 'Retry_3_2', 'control_failed': 'Retry_3_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'SafePositionConveyor', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:613 y:26
			OperatableStateMachine.add('Retry_3_2',
										WaitState(wait_time=3),
										transitions={'done': 'SafePosition_Conveyor'},
										autonomy={'done': Autonomy.Off})

			# x:1479 y:517
			OperatableStateMachine.add('SafePosition_Conveyor_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'Retry_3_2_2', 'control_failed': 'Retry_3_2_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'SafePositionConveyor', 'move_group': 'move_group_gantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1700 y:541
			OperatableStateMachine.add('Retry_3_2_2',
										WaitState(wait_time=3),
										transitions={'done': 'SafePosition_Conveyor_2'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
