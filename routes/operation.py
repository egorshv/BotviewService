from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.operation import operation_keyboard
from keyboards.portfolio import create_portfolio_keyboard
from schemas.operation import OperationSchema
from services.APIHandler import APIHandler
from states.operation import AddForm, GetForm, DeleteForm, UpdateForm
from utils.crud import get_user_portfolios, get_portfolio_by_name, get_operation_list

router = Router()


# ---------- Add operation

@router.message(Command('add_operation'))
async def add_operation_handler(message: Message, state: FSMContext):
    await state.set_state(AddForm.portfolio_name)
    portfolios = await get_user_portfolios(user_id=message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(AddForm.portfolio_name)
async def getting_operation_portfolio_name_handler(message: Message, state: FSMContext):
    await state.set_state(AddForm.operation_value)
    portfolio = await get_portfolio_by_name(
        name=message.text,
        user_id=message.from_user.id
    )
    await state.update_data(portfolio_id=portfolio.id)
    await message.answer(
        'Enter operation value: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(AddForm.operation_value)
async def getting_operation_value_handler(message: Message, state: FSMContext):
    data = await state.update_data(value=float(message.text), created_at=datetime.now())
    operation = OperationSchema(**data)
    await APIHandler().post_object(OperationSchema, operation)
    await state.clear()
    await message.answer(
        'Operation added',
        reply_markup=ReplyKeyboardRemove()
    )


# ---------- Get operations

@router.message(Command('get_operations'))
async def get_operations_handler(message: Message, state: FSMContext):
    await state.set_state(GetForm.operation_portfolio_name)
    portfolios = await get_user_portfolios(user_id=message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(GetForm.operation_portfolio_name)
async def getting_operation_portfolio_name_handler(message: Message, state: FSMContext):
    portfolio = await get_portfolio_by_name(
        name=message.text,
        user_id=message.from_user.id
    )
    operations = await get_operation_list(portfolio_id=portfolio.id)
    operation_pattern = 'id: {} | value: {} | created at: {}'
    operation_string = '\n'.join([operation_pattern.format(
        operation.id,
        operation.value,
        operation.created_at
    ) for operation in operations])
    msg = 'Not operations yet' if not operations else operation_string
    await message.answer(
        msg,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


# ---------- Delete operations

@router.message(Command('delete_operation'))
async def delete_operation_handler(message: Message, state: FSMContext):
    await state.set_state(DeleteForm.operation_portfolio_name)
    portfolios = await get_user_portfolios(user_id=message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(DeleteForm.operation_portfolio_name)
async def getting_operation_portfolio_name_handler(message: Message, state: FSMContext):
    await state.set_state(DeleteForm.operation_id)
    portfolio = await get_portfolio_by_name(
        name=message.text,
        user_id=message.from_user.id
    )
    operations = await get_operation_list(portfolio_id=portfolio.id)
    keyboard = operation_keyboard(operations)
    await message.answer(
        'Choose deleting operation: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(DeleteForm.operation_id)
async def getting_deleting_operation_id_handler(message: Message, state: FSMContext):
    msg = message.text
    operation_id = int(msg[4:msg.index('|') - 1])
    await APIHandler().delete_object(OperationSchema, operation_id)
    await message.answer(
        'Operation deleted',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


# ---------- Update operations

@router.message(Command('update_operation'))
async def update_operation_handler(message: Message, state: FSMContext):
    await state.set_state(UpdateForm.operation_portfolio_name)
    portfolios = await get_user_portfolios(user_id=message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(UpdateForm.operation_portfolio_name)
async def getting_updating_operation_portfolio_name_handler(message: Message, state: FSMContext):
    await state.set_state(UpdateForm.operation_id)
    portfolio = await get_portfolio_by_name(
        name=message.text,
        user_id=message.from_user.id
    )
    operations = await get_operation_list(portfolio_id=portfolio.id)
    await state.update_data(portfolio_id=portfolio.id)
    keyboard = operation_keyboard(operations)
    await message.answer(
        'Choose updating operation: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(UpdateForm.operation_id)
async def getting_updating_operation_id_handler(message: Message, state: FSMContext):
    await state.set_state(UpdateForm.operation_value)
    msg = message.text
    operation_id = int(msg[4:msg.index('|')])
    await state.update_data(id=operation_id)
    await message.answer(
        'Enter new operation value: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.operation_value)
async def getting_updating_operation_value_handler(message: Message, state: FSMContext):
    data = await state.update_data(value=float(message.text), created_at=datetime.now())
    operation = OperationSchema(**data)
    await APIHandler().update_object(OperationSchema, operation.id, operation)
    await message.answer(
        'Operation updated',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
