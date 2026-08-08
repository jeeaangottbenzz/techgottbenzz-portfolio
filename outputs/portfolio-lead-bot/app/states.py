from aiogram.fsm.state import State, StatesGroup


class LeadForm(StatesGroup):
    service = State()
    description = State()
    budget = State()
    deadline = State()
    contact = State()
    confirmation = State()

