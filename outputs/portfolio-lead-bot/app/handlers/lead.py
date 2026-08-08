import logging

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..config import Config
from ..database import Database, LeadRateLimitError
from ..formatters import admin_lead_message, lead_summary
from ..keyboards import (
    BUDGETS,
    SERVICES,
    back_to_menu_keyboard,
    budget_keyboard,
    confirmation_keyboard,
    contact_keyboard,
    main_menu,
    service_keyboard,
)
from ..states import LeadForm
from ..texts import (
    ASK_BUDGET,
    ASK_CONTACT,
    ASK_DEADLINE,
    ASK_DESCRIPTION,
    ASK_SERVICE,
    CANCELLED,
    CONFIRMATION,
)


router = Router(name="lead")
logger = logging.getLogger(__name__)


async def show_confirmation(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.set_state(LeadForm.confirmation)
    await message.answer(
        CONFIRMATION.format(summary=lead_summary(data)),
        reply_markup=confirmation_keyboard(),
    )


@router.callback_query(F.data == "lead:start")
async def start_lead(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(LeadForm.service)
    if callback.message:
        await callback.message.edit_text(ASK_SERVICE, reply_markup=service_keyboard())
    await callback.answer()


@router.callback_query(LeadForm.service, F.data.startswith("lead:service:"))
async def choose_service(callback: CallbackQuery, state: FSMContext) -> None:
    key = callback.data.rsplit(":", 1)[-1]
    service = SERVICES.get(key)
    if service is None:
        await callback.answer("Выберите услугу из списка.", show_alert=True)
        return
    await state.update_data(service=service)
    await state.set_state(LeadForm.description)
    if callback.message:
        await callback.message.edit_text(ASK_DESCRIPTION)
    await callback.answer()


@router.message(LeadForm.description)
async def receive_description(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if len(value) < 10:
        await message.answer("Опишите задачу чуть подробнее — минимум 10 символов.")
        return
    if len(value) > 2000:
        await message.answer("Описание слишком длинное. Сократите его до 2000 символов.")
        return
    await state.update_data(description=value)
    await state.set_state(LeadForm.budget)
    await message.answer(ASK_BUDGET, reply_markup=budget_keyboard())


@router.callback_query(LeadForm.budget, F.data.startswith("lead:budget:"))
async def choose_budget(callback: CallbackQuery, state: FSMContext) -> None:
    key = callback.data.rsplit(":", 1)[-1]
    budget = BUDGETS.get(key)
    if budget is None:
        await callback.answer("Выберите бюджет из списка.", show_alert=True)
        return
    await state.update_data(budget=budget)
    await state.set_state(LeadForm.deadline)
    if callback.message:
        await callback.message.edit_text(ASK_DEADLINE)
    await callback.answer()


@router.message(LeadForm.deadline)
async def receive_deadline(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if len(value) < 2 or len(value) > 200:
        await message.answer("Укажите срок коротким сообщением — до 200 символов.")
        return
    await state.update_data(deadline=value)
    await state.set_state(LeadForm.contact)
    await message.answer(
        ASK_CONTACT, reply_markup=contact_keyboard(message.from_user.username)
    )


@router.message(LeadForm.contact)
async def receive_contact(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if len(value) < 4 or len(value) > 200:
        await message.answer("Отправьте корректный @username или номер телефона.")
        return
    await state.update_data(contact=value)
    await show_confirmation(message, state)


@router.callback_query(LeadForm.contact, F.data == "lead:contact:telegram")
async def use_telegram_contact(callback: CallbackQuery, state: FSMContext) -> None:
    username = callback.from_user.username
    if not username:
        await callback.answer("Укажите @username или телефон сообщением.", show_alert=True)
        return
    await state.update_data(contact=f"@{username}")
    if callback.message:
        await show_confirmation(callback.message, state)
    await callback.answer()


@router.callback_query(LeadForm.confirmation, F.data == "lead:change")
async def change_lead(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(LeadForm.service)
    if callback.message:
        await callback.message.edit_text(ASK_SERVICE, reply_markup=service_keyboard())
    await callback.answer()


@router.callback_query(F.data == "lead:cancel")
async def cancel_lead(callback: CallbackQuery, state: FSMContext, config: Config) -> None:
    await state.clear()
    if callback.message:
        await callback.message.edit_text(
            CANCELLED, reply_markup=main_menu(config.personal_telegram_url)
        )
    await callback.answer()


@router.callback_query(LeadForm.confirmation, F.data == "lead:confirm")
async def confirm_lead(
    callback: CallbackQuery,
    state: FSMContext,
    db: Database,
    config: Config,
    bot: Bot,
) -> None:
    data = await state.get_data()
    payload = {
        **data,
        "user_id": callback.from_user.id,
        "username": callback.from_user.username,
    }
    try:
        lead_id = await db.create_lead(payload)
    except LeadRateLimitError:
        await state.clear()
        if callback.message:
            await callback.message.edit_text(
                "Заявка уже отправлена. Чтобы защитить бота от повторных отправок, "
                "новую заявку можно оставить через минуту.",
                reply_markup=back_to_menu_keyboard(),
            )
        await callback.answer("Заявка уже принята", show_alert=True)
        return
    await state.clear()

    if callback.message:
        await callback.message.edit_text(
            f"✅ <b>Заявка №{lead_id} принята</b>\n\n"
            "Никита получил информацию и свяжется с вами по указанному контакту.",
            reply_markup=back_to_menu_keyboard(),
        )

    if config.admin_id:
        try:
            await bot.send_message(
                config.admin_id,
                admin_lead_message(payload, lead_id),
                disable_web_page_preview=True,
            )
        except Exception:
            logger.exception("Не удалось отправить уведомление администратору")
    else:
        logger.warning(
            "ADMIN_ID равен 0: заявка №%s сохранена без уведомления администратора",
            lead_id,
        )
    await callback.answer("Заявка отправлена")
