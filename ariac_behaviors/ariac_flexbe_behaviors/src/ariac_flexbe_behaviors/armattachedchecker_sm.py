#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.Check_Gripper_attached import CheckGripperattached
from ariac_support_flexbe_states.replace_state import ReplaceState
from flexbe_states.log_state import LogState
from flexbe_states.log_key_state import LogKeyState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 28 2020
@author: Stijn van Hest
'''
class ArmattachedcheckerSM(Behavior):
	'''
	Deze behaivoir check of de armen allebei iets vast heeft, als dat niet zo is zet hij de arm_id naar de arm die nog niks vast heeft
	'''


	def __init__(self):
		super(ArmattachedcheckerSM, self).__init__()
		self.name = 'Armattachedchecker'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1534 y:100, x:62 y:356
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['ARMidMAIN', 'BothArmsFull', 'BothArmsEMPTY'])
		_state_machine.userdata.arm_idR = 'right_arm'
		_state_machine.userdata.arm_idL = 'left_arm'
		_state_machine.userdata.ARMidMAIN = ''
		_state_machine.userdata.BothArmsFull = ''
		_state_machine.userdata.Ja_value = 'Ja'
		_state_machine.userdata.Nee_value = 'Nee'
		_state_machine.userdata.BothArmsEMPTY = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:70 y:32
			OperatableStateMachine.add('CheckGripperRight',
										CheckGripperattached(),
										transitions={'True': 'CheckGripperLeft', 'False': 'CheckGripperLeft_2', 'invalid_arm_id': 'failed'},
										autonomy={'True': Autonomy.Off, 'False': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idR'})

			# x:69 y:94
			OperatableStateMachine.add('CheckGripperLeft',
										CheckGripperattached(),
										transitions={'True': 'SetBothArmFull', 'False': 'ResetBothArmFull', 'invalid_arm_id': 'failed'},
										autonomy={'True': Autonomy.Off, 'False': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idL'})

			# x:702 y:22
			OperatableStateMachine.add('SetArmRight',
										ReplaceState(),
										transitions={'done': 'LogRighterarm'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'arm_idR', 'result': 'ARMidMAIN'})

			# x:702 y:85
			OperatableStateMachine.add('SetArmLeft',
										ReplaceState(),
										transitions={'done': 'LogLeftArm'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'arm_idL', 'result': 'ARMidMAIN'})

			# x:528 y:142
			OperatableStateMachine.add('SetBothArmFull',
										ReplaceState(),
										transitions={'done': 'BothArmsFullLOG'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Ja_value', 'result': 'BothArmsFull'})

			# x:888 y:19
			OperatableStateMachine.add('LogRighterarm',
										LogState(text="The Right arm has nothing attached to it", severity=Logger.REPORT_HINT),
										transitions={'done': 'Arm_id is:'},
										autonomy={'done': Autonomy.Off})

			# x:887 y:77
			OperatableStateMachine.add('LogLeftArm',
										LogState(text="The Left arm has nothing attached to it", severity=Logger.REPORT_HINT),
										transitions={'done': 'Arm_id is:'},
										autonomy={'done': Autonomy.Off})

			# x:530 y:84
			OperatableStateMachine.add('ResetBothArmFull',
										ReplaceState(),
										transitions={'done': 'SetArmLeft'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Nee_value', 'result': 'BothArmsFull'})

			# x:530 y:26
			OperatableStateMachine.add('ResetBothArmFull_2',
										ReplaceState(),
										transitions={'done': 'SetArmRight'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Nee_value', 'result': 'BothArmsFull'})

			# x:1149 y:41
			OperatableStateMachine.add('Arm_id is:',
										LogKeyState(text="The chosen arm_id is:{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'BothArmsFullLOG'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'ARMidMAIN'})

			# x:1365 y:90
			OperatableStateMachine.add('BothArmsFullLOG',
										LogKeyState(text='Zijn beide armen vol: {}', severity=Logger.REPORT_HINT),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'BothArmsFull'})

			# x:300 y:28
			OperatableStateMachine.add('CheckGripperLeft_2',
										CheckGripperattached(),
										transitions={'True': 'ResetBothArmFull_2', 'False': 'SetBothArmEMPTY', 'invalid_arm_id': 'failed'},
										autonomy={'True': Autonomy.Off, 'False': Autonomy.Off, 'invalid_arm_id': Autonomy.Off},
										remapping={'arm_id': 'arm_idL'})

			# x:319 y:412
			OperatableStateMachine.add('SetBothArmEMPTY',
										ReplaceState(),
										transitions={'done': 'ResetBothArmFull_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Ja_value', 'result': 'BothArmsEMPTY'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
