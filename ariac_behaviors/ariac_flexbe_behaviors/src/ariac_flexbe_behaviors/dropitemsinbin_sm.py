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
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_flexbe_states.Check_Gripper_attached import CheckGripperattached
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_behaviors.startup_sm import StartUPSM
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_flexbe_states.Compute_belt_drop import ComputeBeltDrop
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 01 2020
@author: Stijn van Hest
'''
class DropItemsInBINSM(Behavior):
	'''
	This behavoir drops both items in the bins
	'''


	def __init__(self):
		super(DropItemsInBINSM, self).__init__()
		self.name = 'DropItemsInBIN'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(StartUPSM, 'StartUP')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1249 y:486, x:614 y:299, x:1274 y:293, x:1759 y:363
		_state_machine = OperatableStateMachine(outcomes=['Next arm', 'failed', 'BothArmsEmpty', 'BinVol'], input_keys=['USEarmID', 'GantryLocation', 'RightArmItem', 'LeftArmItem'], output_keys=['RightArmItem', 'LeftArmItem'])
		_state_machine.userdata.arm_idL = 'left_arm'
		_state_machine.userdata.arm_idR = 'right_arm'
		_state_machine.userdata.USEarmID = ''
		_state_machine.userdata.move_groupR = 'Right_Arm'
		_state_machine.userdata.move_groupL = 'Left_Arm'
		_state_machine.userdata.tool_linkL = 'left_ee_link'
		_state_machine.userdata.tool_linkR = 'right_ee_link'
		_state_machine.userdata.DropPose = []
		_state_machine.userdata.offsetXPiston = 0
		_state_machine.userdata.offsetPiston = 0
		_state_machine.userdata.offsetYPiston = 0
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.PistonOffset = 0.22
		_state_machine.userdata.GasketOffset = 0.15
		_state_machine.userdata.offsetGasket = 0
		_state_machine.userdata.offsetXGasket = -0.1
		_state_machine.userdata.offsetYGasket = 0
		_state_machine.userdata.GasketLocation = 'GasketLoc'
		_state_machine.userdata.PistonLocation = 'PistonLoc'
		_state_machine.userdata.GantryLocation = ''
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.Niks = 'Niks'
		_state_machine.userdata.RightArmItem = ''
		_state_machine.userdata.LeftArmItem = ''
		_state_machine.userdata.SideXoffset = 0
		_state_machine.userdata.SideYoffset = 0
		_state_machine.userdata.SideZoffset = 0
		_state_machine.userdata.GasketRow = 0
		_state_machine.userdata.PistonRow = 0
		_state_machine.userdata.RowTarget = 4
		_state_machine.userdata.GasketRound = 0
		_state_machine.userdata.PistonRound = 0
		_state_machine.userdata.RoundTarget = 12
		_state_machine.userdata.Zero_Value = 0
		_state_machine.userdata.One_value = 1
		_state_machine.userdata.move_groupG = 'Gantry'
		_state_machine.userdata.config_nameSH3 = 'Gantry_SafeHall3'
		_state_machine.userdata.robot_name = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:47 y:31
			OperatableStateMachine.add('GasketLocation',
										EqualState(),
										transitions={'true': 'GetGasketBinPosition', 'false': 'PistonLocation'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'GasketLocation', 'value_b': 'GantryLocation'})

			# x:216 y:33
			OperatableStateMachine.add('GetGasketBinPosition',
										GetObjectPoseState(object_frame='bin12_frame', ref_frame='world'),
										transitions={'continue': 'SetGasketBinXOffset', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'DropPose'})

			# x:208 y:544
			OperatableStateMachine.add('GetPistonBinPosition',
										GetObjectPoseState(object_frame='bin1_frame', ref_frame='world'),
										transitions={'continue': 'SetPistonBinYOffset', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'DropPose'})

			# x:1363 y:346
			OperatableStateMachine.add('checkLeftArmAttached',
										CheckGripperattached(),
										transitions={'True': 'Next arm', 'False': 'BothArmsEmpty', 'invalid_arm_id': 'failed'},
										autonomy={'True': Autonomy.Off, 'False': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idL'})

			# x:1028 y:38
			OperatableStateMachine.add('GripperUITRechts',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'ResetRightArmItem', 'failed': 'GoToDropRight', 'invalid_arm_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idR'})

			# x:848 y:38
			OperatableStateMachine.add('GoToDropRight',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GripperUITRechts', 'planning_failed': 'GripperUITRechts', 'control_failed': 'GripperUITRechts'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupR', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1563 y:393
			OperatableStateMachine.add('StartUP',
										self.use_behavior(StartUPSM, 'StartUP'),
										transitions={'finished': 'checkRightArmAttached', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:1203 y:37
			OperatableStateMachine.add('ResetRightArmItem',
										ReplaceState(),
										transitions={'done': 'AddX2offsetGasket'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Niks', 'result': 'RightArmItem'})

			# x:1029 y:100
			OperatableStateMachine.add('GripperUITLinks',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'ResetLeftArmItem', 'failed': 'GoToDropLeft', 'invalid_arm_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idL'})

			# x:44 y:542
			OperatableStateMachine.add('PistonLocation',
										EqualState(),
										transitions={'true': 'GetPistonBinPosition', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'PistonLocation', 'value_b': 'GantryLocation'})

			# x:848 y:98
			OperatableStateMachine.add('GoToDropLeft',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GripperUITLinks', 'planning_failed': 'GripperUITLinks', 'control_failed': 'GripperUITLinks'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupL', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1203 y:100
			OperatableStateMachine.add('ResetLeftArmItem',
										ReplaceState(),
										transitions={'done': 'AddX2offsetGasket'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Niks', 'result': 'LeftArmItem'})

			# x:1359 y:423
			OperatableStateMachine.add('checkRightArmAttached',
										CheckGripperattached(),
										transitions={'True': 'Next arm', 'False': 'checkLeftArmAttached', 'invalid_arm_id': 'failed'},
										autonomy={'True': Autonomy.Off, 'False': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idR'})

			# x:708 y:35
			OperatableStateMachine.add('ComputeRightDrop',
										ComputeBeltDrop(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'GoToDropRight', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupR', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_linkR', 'pose': 'DropPose', 'offset': 'SideZoffset', 'SideYoffset': 'SideYoffset', 'SideXoffset': 'SideXoffset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:706 y:99
			OperatableStateMachine.add('ComputeLeftDrop',
										ComputeBeltDrop(joint_names=['left_shoulder_pan_joint', 'left_shoulder_lift_joint', 'left_elbow_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'GoToDropLeft', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupL', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_linkL', 'pose': 'DropPose', 'offset': 'SideZoffset', 'SideYoffset': 'SideYoffset', 'SideXoffset': 'SideXoffset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:365 y:34
			OperatableStateMachine.add('SetGasketBinXOffset',
										ReplaceState(),
										transitions={'done': 'SetGasketBinYOffset'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'offsetXGasket', 'result': 'SideXoffset'})

			# x:362 y:99
			OperatableStateMachine.add('SetGasketBinYOffset',
										ReplaceState(),
										transitions={'done': 'RechterARM?2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'offsetYGasket', 'result': 'SideYoffset'})

			# x:350 y:606
			OperatableStateMachine.add('SetPistonBinXOffset',
										ReplaceState(),
										transitions={'done': 'RechterARM?'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'offsetXPiston', 'result': 'SideXoffset'})

			# x:352 y:544
			OperatableStateMachine.add('SetPistonBinYOffset',
										ReplaceState(),
										transitions={'done': 'SetPistonBinXOffset'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'offsetYPiston', 'result': 'SideYoffset'})

			# x:1378 y:35
			OperatableStateMachine.add('AddX2offsetGasket',
										AddNumericState(),
										transitions={'done': 'CheckGasketRows'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'offsetXGasket', 'value_b': 'GasketOffset', 'result': 'offsetXGasket'})

			# x:1378 y:98
			OperatableStateMachine.add('CheckGasketRows',
										EqualState(),
										transitions={'true': 'ResetGasketRow', 'false': 'AddGasketRound'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'GasketRound', 'value_b': 'RowTarget'})

			# x:1376 y:158
			OperatableStateMachine.add('ResetGasketRow',
										ReplaceState(),
										transitions={'done': 'AddYoffsetGasket'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Zero_Value', 'result': 'offsetXGasket'})

			# x:1373 y:220
			OperatableStateMachine.add('AddYoffsetGasket',
										AddNumericState(),
										transitions={'done': 'AddGasketRound'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'GasketOffset', 'value_b': 'offsetYGasket', 'result': 'offsetYGasket'})

			# x:1551 y:37
			OperatableStateMachine.add('AddGasketRound',
										AddNumericState(),
										transitions={'done': 'CheckGasketRound'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'One_value', 'value_b': 'GasketRound', 'result': 'GasketRound'})

			# x:1551 y:102
			OperatableStateMachine.add('CheckGasketRound',
										EqualState(),
										transitions={'true': 'ResetGasketRound', 'false': 'BackToSH3'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'GasketRound', 'value_b': 'RoundTarget'})

			# x:1717 y:103
			OperatableStateMachine.add('ResetGasketRound',
										ReplaceState(),
										transitions={'done': 'BinVol'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Zero_Value', 'result': 'offsetYGasket'})

			# x:534 y:33
			OperatableStateMachine.add('RechterARM?2',
										EqualState(),
										transitions={'true': 'ComputeRightDrop', 'false': 'ComputeLeftDrop'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'USEarmID', 'value_b': 'arm_idR'})

			# x:518 y:544
			OperatableStateMachine.add('RechterARM?',
										EqualState(),
										transitions={'true': 'ComputeRightDrop_2', 'false': 'ComputeLeftDrop_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'USEarmID', 'value_b': 'arm_idR'})

			# x:689 y:544
			OperatableStateMachine.add('ComputeRightDrop_2',
										ComputeBeltDrop(joint_names=['right_shoulder_pan_joint', 'right_shoulder_lift_joint', 'right_elbow_joint', 'right_wrist_1_joint', 'right_wrist_2_joint', 'right_wrist_3_joint']),
										transitions={'continue': 'GoToDropRight_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupR', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_linkR', 'pose': 'DropPose', 'offset': 'SideZoffset', 'SideYoffset': 'SideYoffset', 'SideXoffset': 'SideXoffset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:688 y:609
			OperatableStateMachine.add('ComputeLeftDrop_2',
										ComputeBeltDrop(joint_names=['left_shoulder_pan_joint', 'left_shoulder_lift_joint', 'left_elbow_joint', 'left_wrist_1_joint', 'left_wrist_2_joint', 'left_wrist_3_joint']),
										transitions={'continue': 'GoToDropLeft_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_groupL', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_linkL', 'pose': 'DropPose', 'offset': 'SideZoffset', 'SideYoffset': 'SideYoffset', 'SideXoffset': 'SideXoffset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:836 y:545
			OperatableStateMachine.add('GoToDropRight_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GripperUITRechts_2', 'planning_failed': 'GripperUITRechts_2', 'control_failed': 'GripperUITRechts_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupR', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:834 y:607
			OperatableStateMachine.add('GoToDropLeft_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GripperUITLinks_2', 'planning_failed': 'GripperUITLinks_2', 'control_failed': 'GripperUITLinks_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_groupL', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1008 y:547
			OperatableStateMachine.add('GripperUITRechts_2',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'ResetRightArmItem_2', 'failed': 'GoToDropRight_2', 'invalid_arm_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idR'})

			# x:1008 y:606
			OperatableStateMachine.add('GripperUITLinks_2',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'ResetLeftArmItem_2', 'failed': 'GoToDropLeft_2', 'invalid_arm_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idL'})

			# x:1173 y:549
			OperatableStateMachine.add('ResetRightArmItem_2',
										ReplaceState(),
										transitions={'done': 'AddX2offsetPiston'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Niks', 'result': 'RightArmItem'})

			# x:1173 y:607
			OperatableStateMachine.add('ResetLeftArmItem_2',
										ReplaceState(),
										transitions={'done': 'AddX2offsetPiston'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Niks', 'result': 'LeftArmItem'})

			# x:1343 y:550
			OperatableStateMachine.add('AddX2offsetPiston',
										AddNumericState(),
										transitions={'done': 'CheckPistonRows'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'offsetXPiston', 'value_b': 'PistonOffset', 'result': 'offsetXPiston'})

			# x:1517 y:602
			OperatableStateMachine.add('CheckPistonRound',
										EqualState(),
										transitions={'true': 'ResetPistonRound', 'false': 'StartUP'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'PistonRound', 'value_b': 'RoundTarget'})

			# x:1343 y:615
			OperatableStateMachine.add('CheckPistonRows',
										EqualState(),
										transitions={'true': 'ResetPistonRow', 'false': 'AddPistonRound'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'PistonRound', 'value_b': 'RowTarget'})

			# x:1342 y:676
			OperatableStateMachine.add('ResetPistonRow',
										ReplaceState(),
										transitions={'done': 'AddYoffsetPiston'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Zero_Value', 'result': 'offsetXPiston'})

			# x:1340 y:735
			OperatableStateMachine.add('AddYoffsetPiston',
										AddNumericState(),
										transitions={'done': 'AddPistonRound'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'PistonOffset', 'value_b': 'offsetYPiston', 'result': 'offsetYPiston'})

			# x:1514 y:669
			OperatableStateMachine.add('AddPistonRound',
										AddNumericState(),
										transitions={'done': 'CheckPistonRound'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'One_value', 'value_b': 'PistonRound', 'result': 'PistonRound'})

			# x:1688 y:602
			OperatableStateMachine.add('ResetPistonRound',
										ReplaceState(),
										transitions={'done': 'BinVol'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Zero_Value', 'result': 'offsetYPiston'})

			# x:1559 y:228
			OperatableStateMachine.add('BackToSH3',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'StartUP', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_nameSH3', 'move_group': 'move_groupG', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
