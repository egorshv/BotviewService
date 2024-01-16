from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiohttp import ClientConnectionError
from pydantic import ValidationError

from callbacks.operation import OperationCallback
from callbacks.portfolio import PortfolioCallback
from keyboards.KeyboardCreator import KeyboardCreator
from schemas.operation import OperationSchema
from services.UserStorageManager import UserStorageManager
from states.operation import AddForm, DeleteForm, UpdateForm
from utils.validators import isfloat

router = Router()


# ---------- Add operation

@router.message(Command('add_operation'))
async def add_operation_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator().create_portfolio_keyboard(portfolios, 'operation-add')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'operation-add'))
async def get_portfolio_id_callback(query: CallbackQuery, callback_data: PortfolioCallback, state: FSMContext):
    await state.set_state(AddForm.operation_value)
    await state.update_data(portfolio_id=callback_data.id)
    await query.message.answer(
        'Enter operation value: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(AddForm.operation_value)
async def getting_operation_value_handler(message: Message, state: FSMContext):
    if not isfloat(message.text):
        await message.answer(
            'Wrong field value, try again',
            reply_markup=ReplyKeyboardRemove()
        )
        return await state.set_state(AddForm.operation_value)
    try:
        data = await state.update_data(value=float(message.text), created_at=datetime.now())
        operation = OperationSchema(**data)
        await UserStorageManager(user_id=message.from_user.id).add_operation(operation)
        await message.answer(
            'Operation added',
            reply_markup=ReplyKeyboardRemove()
        )
    except ValidationError:
        await message.answer(
            'Validation error, try again',
            reply_markup=ReplyKeyboardRemove()
        )
    except ClientConnectionError:
        await message.answer(
            'Network error, try again',
            reply_markup=ReplyKeyboardRemove()
        )
    finally:
        await state.clear()


# ---------- Get operations

@router.message(Command('get_operations'))
async def get_operations_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator.create_portfolio_keyboard(portfolios, 'operation-get')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'operation-get'))
async def getting_portfolio_id_handler(query: CallbackQuery, callback_data: PortfolioCallback):
    operations = await UserStorageManager(user_id=query.message.from_user.id).get_operations(
        portfolio_id=callback_data.id
    )
    operation_string = '\n'.join(list(map(str, operations)))
    msg = 'Not operations yet' if not operations else operation_string
    await query.message.answer(
        msg,
        reply_markup=ReplyKeyboardRemove()
    )


# ---------- Delete operations

@router.message(Command('delete_operation'))
async def delete_operation_handler(message: Message, state: FSMContext):
    await state.set_state(DeleteForm.operation_portfolio_name)
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator.create_portfolio_keyboard(portfolios, 'operation-delete')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'operation-delete'))
async def getting_portfolio_id_callback(query: CallbackQuery, callback_data: PortfolioCallback):
    operations = await UserStorageManager(user_id=query.message.from_user.id).get_operations(
        portfolio_id=callback_data.id
    )
    keyboard = KeyboardCreator().create_operation_keyboard(operations, 'operation-delete')
    await query.message.answer(
        'Choose deleting operation: ',
        reply_markup=keyboard
    )


@router.callback_query(OperationCallback.filter(F.type == 'operation-delete'))
async def getting_operation_id_callback(query: CallbackQuery, callback_data: OperationCallback):
    await UserStorageManager(user_id=query.message.from_user.id).delete_operation(callback_data.id)
    await query.message.answer(
        'Operation deleted',
        reply_markup=ReplyKeyboardRemove()
    )


# ---------- Update operations

@router.message(Command('update_operation'))
async def update_operation_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator().create_portfolio_keyboard(portfolios, 'operation-update')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'operation-update'))
async def getting_portfolio_id_callback(query: CallbackQuery, callback_data: PortfolioCallback, state: FSMContext):
    await state.set_state(UpdateForm.operation_value)
    await state.update_data(portfolio_id=callback_data.id)
    operations = await UserStorageManager(user_id=query.message.from_user.id).get_operations(
        portfolio_id=callback_data.id
    )
    keyboard = KeyboardCreator().create_operation_keyboard(operations, 'update')
    await query.message.answer(
        'Choose updating operation: ',
        reply_markup=keyboard
    )


@router.callback_query(OperationCallback.filter(F.type == 'update'))
async def getting_updating_operation_callback(query: CallbackQuery, callback_data: OperationCallback,
                                              state: FSMContext):
    await state.set_state(UpdateForm.operation_value)
    await state.update_data(id=callback_data.id)
    await query.message.answer(
        'Enter new operation value: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.operation_value)
async def getting_updating_operation_value_handler(message: Message, state: FSMContext):
    if not isfloat(message.text):
        await message.answer(
            'Wrong field value, try again',
            reply_markup=ReplyKeyboardRemove()
        )
        return await state.set_state(UpdateForm.operation_value)
    try:
        data = await state.update_data(value=float(message.text), created_at=datetime.now())
        operation = OperationSchema(**data)
        await UserStorageManager(user_id=message.from_user.id).update_operation(operation.id, operation)
        await message.answer(
            'Operation updated',
            reply_markup=ReplyKeyboardRemove()
        )
    except ValidationError:
        await message.answer(
            'Validation error, try again',
            reply_markup=ReplyKeyboardRemove()
        )
    except ClientConnectionError:
        await message.answer(
            'Network error, try again',
            reply_markup=ReplyKeyboardRemove()
        )
    finally:
        await state.clear()
