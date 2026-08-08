from aiogram.fsm.state import State, StatesGroup


class CheckoutStates(StatesGroup):
    entering_name = State()
    entering_phone = State()
    choosing_fulfillment = State()
    entering_location = State()
    entering_comment = State()
    reviewing = State()

