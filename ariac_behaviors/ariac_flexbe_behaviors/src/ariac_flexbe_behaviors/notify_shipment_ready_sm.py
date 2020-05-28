#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.notify_shipment_ready_state import NotifyShipmentReadyState
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.get_agv_status_state import GetAgvStatusState
from ariac_support_flexbe_states.equal_state import EqualState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed May 27 2020
@author: Anne van Oirschot
'''
class Notify_Shipment_ReadySM(Behavior):
	'''
	AGV verzenden voor transport
	'''


	def __init__(self):
		super(Notify_Shipment_ReadySM, self).__init__()
		self.name = 'Notify_Shipment_Ready'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:694 y:154, x:184 y:197
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['agv_id', 'shipment_type'])
		_state_machine.userdata.agv_id = ""
		_state_machine.userdata.shipment_type = ""
		_state_machine.userdata.success = 0
		_state_machine.userdata.agv_state = ""
		_state_machine.userdata.agv_ready_state = "ready_to_deliver"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:60 y:39
			OperatableStateMachine.add('NotifyShipmentReady',
										NotifyShipmentReadyState(),
										transitions={'continue': 'Wait', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'agv_id': 'agv_id', 'shipment_type': 'shipment_type', 'success': 'success', 'message': 'message'})

			# x:259 y:43
			OperatableStateMachine.add('Wait',
										WaitState(wait_time=1),
										transitions={'done': 'GetAgvState'},
										autonomy={'done': Autonomy.Off})

			# x:438 y:42
			OperatableStateMachine.add('GetAgvState',
										GetAgvStatusState(),
										transitions={'continue': 'AgvReady', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'agv_id': 'agv_id', 'agv_state': 'agv_state'})

			# x:442 y:148
			OperatableStateMachine.add('AgvReady',
										EqualState(),
										transitions={'true': 'finished', 'false': 'Wait'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_state', 'value_b': 'agv_ready_state'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
