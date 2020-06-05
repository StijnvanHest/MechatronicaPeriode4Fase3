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
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from flexbe_states.wait_state import WaitState
from ariac_support_flexbe_states.replace_state import ReplaceState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri May 29 2020
@author: Stijn van Hest
'''
class GoToPreDropSM(Behavior):
	'''
	This behaivor goes to the predrop of the parts
	'''


	def __init__(self):
		super(GoToPreDropSM, self).__init__()
		self.name = 'GoToPreDrop'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1917 y:246, x:607 y:792
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['RightArmItem', 'LeftArmItem'], output_keys=['GantryLocation', 'USEarmID'])
		_state_machine.userdata.move_groupG = 'Gantry'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.config_nameGasket = 'Gantry_Bin7_8_inverse'
		_state_machine.userdata.config_nameGasketINV = 'Gantry_Bin7_8'
		_state_machine.userdata.config_namePiston = 'Gantry_Bin15_16_inverse'
		_state_machine.userdata.config_namePistonINV = 'Gantry_Bin15_16'
		_state_machine.userdata.config_nameSHL2 = 'Gantry_SafeHall2'
		_state_machine.userdata.config_nameSHL1 = 'Gantry_SafeHall1'
		_state_machine.userdata.Gasket = 'Gasket'
		_state_machine.userdata.Piston = 'Piston'
		_state_machine.userdata.PartTYPE = ''
		_state_machine.userdata.RightArmItem = ''
		_state_machine.userdata.LeftArmItem = ''
		_state_machine.userdata.GasketLocation = 'GasketLoc'
		_state_machine.userdata.PistonLocation = 'PistonLoc'
		_state_machine.userdata.GantryLocation = ''
		_state_machine.userdata.USEarmID = ''
		_state_machine.userdata.ArmRight = 'right_arm'
		_state_machine.userdata.ArmLeft = 'left_arm'
		_state_machine.userdata.config_nameSHL3 = 'Gantry_SafeHall3'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:75 y:32
			OperatableStateMachine.add('CheckGasketLeftArm?',
										EqualState(),
										transitions={'true': 'SetLeftArmToUse', 'false': 'CheckGasketRightArm?'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'LeftArmItem', 'value_b': 'Gasket'})

			# x:1257 y:313
			OperatableStateMachine.add('GoToPredropPiston',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'SetGantryLocationPiston', 'planning_failed': 'GoPreDropFailed', 'control_failed': 'GoPreDropFailed', 'param_error': 'GoPreDropFailed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_namePiston', 'move_group': 'move_groupG', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:641 y:36
			OperatableStateMachine.add('GoToSafeHall3',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GoToPredropGasket', 'planning_failed': 'waitFailed', 'control_failed': 'GoToSafeHall2_2_2', 'param_error': 'GoToSafeHall2_2_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_nameSHL3', 'move_group': 'move_groupG', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1254 y:439
			OperatableStateMachine.add('GoToPredropPiston_INV',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'SetGantryLocationPiston', 'planning_failed': 'GoPreDropFailed', 'control_failed': 'GoPreDropFailed', 'param_error': 'GoPreDropFailed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_namePistonINV', 'move_group': 'move_groupG', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1257 y:187
			OperatableStateMachine.add('GoToPredropGasket_INV',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'SetGantryLocationGasket', 'planning_failed': 'GoPreDropFailed', 'control_failed': 'GoPreDropFailed', 'param_error': 'GoPreDropFailed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_nameGasket', 'move_group': 'move_groupG', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:648 y:206
			OperatableStateMachine.add('GoToSafeHall2_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GoToPredropPiston', 'planning_failed': 'waitFailed', 'control_failed': 'waitFailed', 'param_error': 'waitFailed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_nameSHL1', 'move_group': 'move_groupG', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:842 y:600
			OperatableStateMachine.add('waitFailed',
										WaitState(wait_time=2),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:72 y:126
			OperatableStateMachine.add('CheckGasketRightArm?',
										EqualState(),
										transitions={'true': 'SetRightArmToUse', 'false': 'CheckPistonLeftARM?'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'RightArmItem', 'value_b': 'Gasket'})

			# x:70 y:328
			OperatableStateMachine.add('CheckPistonRightArm?',
										EqualState(),
										transitions={'true': 'SetRightArmToUse_2', 'false': 'waitFailed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'RightArmItem', 'value_b': 'Piston'})

			# x:70 y:230
			OperatableStateMachine.add('CheckPistonLeftARM?',
										EqualState(),
										transitions={'true': 'SetLeftArmToUse_2', 'false': 'CheckPistonRightArm?'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'LeftArmItem', 'value_b': 'Piston'})

			# x:1562 y:576
			OperatableStateMachine.add('GoPreDropFailed',
										WaitState(wait_time=2),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:1254 y:61
			OperatableStateMachine.add('GoToPredropGasket',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'SetGantryLocationGasket', 'planning_failed': 'GoPreDropFailed', 'control_failed': 'GoPreDropFailed', 'param_error': 'GoPreDropFailed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_nameGasketINV', 'move_group': 'move_groupG', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:649 y:116
			OperatableStateMachine.add('GoToSafeHall3_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GoToPredropGasket_INV', 'planning_failed': 'GoToSafeHall2_2_2', 'control_failed': 'GoToSafeHall2_2_2', 'param_error': 'waitFailed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_nameSHL3', 'move_group': 'move_groupG', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:649 y:326
			OperatableStateMachine.add('GoToSafeHall2_2_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GoToPredropPiston_INV', 'planning_failed': 'waitFailed', 'control_failed': 'waitFailed', 'param_error': 'waitFailed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_nameSHL1', 'move_group': 'move_groupG', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:341 y:33
			OperatableStateMachine.add('SetLeftArmToUse',
										ReplaceState(),
										transitions={'done': 'GoToSafeHall3'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'ArmLeft', 'result': 'USEarmID'})

			# x:353 y:212
			OperatableStateMachine.add('SetLeftArmToUse_2',
										ReplaceState(),
										transitions={'done': 'GoToSafeHall2_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'ArmLeft', 'result': 'USEarmID'})

			# x:361 y:115
			OperatableStateMachine.add('SetRightArmToUse',
										ReplaceState(),
										transitions={'done': 'GoToSafeHall3_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'ArmRight', 'result': 'USEarmID'})

			# x:367 y:318
			OperatableStateMachine.add('SetRightArmToUse_2',
										ReplaceState(),
										transitions={'done': 'GoToSafeHall2_2_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'ArmRight', 'result': 'USEarmID'})

			# x:1600 y:107
			OperatableStateMachine.add('SetGantryLocationGasket',
										ReplaceState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'GasketLocation', 'result': 'GantryLocation'})

			# x:1596 y:370
			OperatableStateMachine.add('SetGantryLocationPiston',
										ReplaceState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'PistonLocation', 'result': 'GantryLocation'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
