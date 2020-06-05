#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_flexbe_behaviors.conveyor_state_sm import Conveyor_StateSM
from ariac_flexbe_states.end_assignment_state import EndAssignment
from ariac_flexbe_behaviors.armattachedchecker_sm import ArmattachedcheckerSM
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_flexbe_behaviors.startup_sm import StartUPSM
from ariac_flexbe_behaviors.beltpickup_sm import BeltPickUPSM
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from flexbe_states.wait_state import WaitState
from ariac_flexbe_behaviors.gotopredrop_sm import GoToPreDropSM
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_flexbe_behaviors.dropitemsinbin_sm import DropItemsInBINSM
from flexbe_states.log_state import LogState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue May 26 2020
@author: Stijn van Hest
'''
class IncomingproductsFULLSM(Behavior):
	'''
	Vul hier je behaivor in en test hem los
	'''


	def __init__(self):
		super(IncomingproductsFULLSM, self).__init__()
		self.name = 'IncomingproductsFULL'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Conveyor_StateSM, 'Conveyor_State')
		self.add_behavior(ArmattachedcheckerSM, 'Armattachedchecker')
		self.add_behavior(StartUPSM, 'StartUP')
		self.add_behavior(BeltPickUPSM, 'BeltPickUP')
		self.add_behavior(GoToPreDropSM, 'GoToPreDrop')
		self.add_behavior(DropItemsInBINSM, 'DropItemsInBIN')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1680 y:94, x:415 y:533
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.move_groupR = 'Right_Arm'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.ARM_idMAIN = ''
		_state_machine.userdata.move_groupL = 'Left_Arm'
		_state_machine.userdata.tool_link_right = 'right_ee_link'
		_state_machine.userdata.tool_link_left = 'left_ee_link'
		_state_machine.userdata.joint_names = ''
		_state_machine.userdata.joint_values = ''
		_state_machine.userdata.ConveyorPartoffset = 0
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.arm_idR = 'right_arm'
		_state_machine.userdata.arm_idL = 'left_arm'
		_state_machine.userdata.Ja_value = 'Ja'
		_state_machine.userdata.Nee_value = 'Nee'
		_state_machine.userdata.BothArmsFull = 'Nee'
		_state_machine.userdata.config_nameLeftPregrasp = 'Left_PreGrasp'
		_state_machine.userdata.config_nameRightPregrasp = 'Right_PreGrasp'
		_state_machine.userdata.config_nameGantryROT = 'Gantry_SafeHall1'
		_state_machine.userdata.move_groupGantry = 'Gantry'
		_state_machine.userdata.Round_nrMAIN = 0
		_state_machine.userdata.RoundTargetMAIN = 4
		_state_machine.userdata.PartTYPE = ''
		_state_machine.userdata.RightArmItem = ''
		_state_machine.userdata.LeftArmItem = ''
		_state_machine.userdata.ONE = 1
		_state_machine.userdata.USEarmID = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('Startass',
										StartAssignment(),
										transitions={'continue': 'ADDround'},
										autonomy={'continue': Autonomy.Off})

			# x:562 y:111
			OperatableStateMachine.add('Conveyor_State',
										self.use_behavior(Conveyor_StateSM, 'Conveyor_State'),
										transitions={'finished': 'BeltPickUP', 'failed': 'WaitFailed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ARMidMAIN': 'ARMidMAIN', 'PartPose': 'PartPose', 'PartOffset': 'PartOffset', 'PartTYPE': 'PartTYPE', 'exactparttype': 'exactparttype'})

			# x:1542 y:89
			OperatableStateMachine.add('stopass',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})

			# x:349 y:41
			OperatableStateMachine.add('Armattachedchecker',
										self.use_behavior(ArmattachedcheckerSM, 'Armattachedchecker'),
										transitions={'finished': 'BothFULL?', 'failed': 'WaitFailed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ARMidMAIN': 'ARMidMAIN', 'BothArmsFull': 'BothArmsFull', 'BothArmsEMPTY': 'BothArmsEMPTY'})

			# x:561 y:45
			OperatableStateMachine.add('BothFULL?',
										EqualState(),
										transitions={'true': 'ToRotationStation', 'false': 'Conveyor_State'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'BothArmsFull', 'value_b': 'Ja_value'})

			# x:179 y:41
			OperatableStateMachine.add('StartUP',
										self.use_behavior(StartUPSM, 'StartUP'),
										transitions={'finished': 'Armattachedchecker', 'failed': 'WaitFailed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:560 y:198
			OperatableStateMachine.add('BeltPickUP',
										self.use_behavior(BeltPickUPSM, 'BeltPickUP'),
										transitions={'finished': 'WaitNewRound', 'failed': 'WaitFailed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ARMidMAIN': 'ARMidMAIN', 'PartPose': 'PartPose', 'PartOffset': 'PartOffset', 'exactparttype': 'exactparttype', 'PartTYPE': 'PartTYPE', 'RightArmItem': 'RightArmItem', 'LeftArmItem': 'LeftArmItem'})

			# x:757 y:46
			OperatableStateMachine.add('ToRotationStation',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GoToPreDrop', 'planning_failed': 'TransfertoDropFailed', 'control_failed': 'TransfertoDropFailed', 'param_error': 'TransfertoDropFailed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_nameGantryROT', 'move_group': 'move_groupGantry', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:203 y:204
			OperatableStateMachine.add('WaitNewRound',
										WaitState(wait_time=0.25),
										transitions={'done': 'StartUP'},
										autonomy={'done': Autonomy.Off})

			# x:376 y:394
			OperatableStateMachine.add('WaitFailed',
										WaitState(wait_time=2),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:749 y:354
			OperatableStateMachine.add('TransfertoDropFailed',
										WaitState(wait_time=2),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:934 y:41
			OperatableStateMachine.add('GoToPreDrop',
										self.use_behavior(GoToPreDropSM, 'GoToPreDrop'),
										transitions={'finished': 'DropItemsInBIN', 'failed': 'TransfertoDropFailed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'RightArmItem': 'RightArmItem', 'LeftArmItem': 'LeftArmItem', 'GantryLocation': 'GantryLocation', 'USEarmID': 'USEarmID'})

			# x:1323 y:153
			OperatableStateMachine.add('RoundCheck',
										EqualState(),
										transitions={'true': 'stopass', 'false': 'ADDround'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'Round_nrMAIN', 'value_b': 'RoundTargetMAIN'})

			# x:21 y:348
			OperatableStateMachine.add('ADDround',
										AddNumericState(),
										transitions={'done': 'StartUP'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'Round_nrMAIN', 'value_b': 'ONE', 'result': 'Round_nrMAIN'})

			# x:1116 y:42
			OperatableStateMachine.add('DropItemsInBIN',
										self.use_behavior(DropItemsInBINSM, 'DropItemsInBIN'),
										transitions={'Next arm': 'GoToPreDrop', 'failed': 'TransfertoDropFailed', 'BothArmsEmpty': 'RoundCheck', 'BinVol': 'LogBinVol'},
										autonomy={'Next arm': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'BothArmsEmpty': Autonomy.Inherit, 'BinVol': Autonomy.Inherit},
										remapping={'USEarmID': 'USEarmID', 'GantryLocation': 'GantryLocation', 'RightArmItem': 'RightArmItem', 'LeftArmItem': 'LeftArmItem'})

			# x:1323 y:46
			OperatableStateMachine.add('LogBinVol',
										LogState(text="Een van de bins is vol", severity=Logger.REPORT_HINT),
										transitions={'done': 'stopass'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
