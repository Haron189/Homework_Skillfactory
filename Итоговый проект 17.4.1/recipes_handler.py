import aiohttp

from aiogram.types import Message
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from random import choices

from googletrans import Translator

router = Router()

class RecipeState(StatesGroup):
    waiting_for_category = State()
    waiting_for_recipe = State()

@router.message(Command("category_search_random"))
async def category_search_random(message: Message, command: CommandObject, state: FSMContext):
    if command.args is None:
        await message.answer(
            "Вы не указали количество рецептов."
        )
        return
    async with aiohttp.ClientSession().get (url=f'https://www.themealdb.com/api/json/v1/1/list.php?c=list') as resp:
               data = await resp.json()
               categories = [category['strCategory'] for category in data['meals']]

    await state.set_data({'categories': categories, 'args': command.args})

    builder = ReplyKeyboardBuilder()
    for date_item in categories:
        builder.add(types.KeyboardButton(text=date_item))
    builder.adjust(5)

    await message.answer(
        f"Выберите категорию: ",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(RecipeState.waiting_for_category.state)

@router.message(RecipeState.waiting_for_category)
async def recipe_by_date(message: types.Message, state: FSMContext):
    data_state = await state.get_data()
    translator = Translator()
    builder = ReplyKeyboardBuilder()

    async with aiohttp.ClientSession().get (url=f'https://www.themealdb.com/api/json/v1/1/filter.php?c={message.text}') as resp:
               data = await resp.json()
               data_choices = choices(data['meals'], k=int(data_state['args']))
               recipes = [recipe['strMeal'] for recipe in data_choices]
               id_recipes = [id_recipe['idMeal'] for id_recipe in data_choices]

    await state.set_data({'id': id_recipes})

    recipes_j = ','.join(map(str, recipes))

    recipe_translator = translator.translate(f'{recipes_j}', dest='ru')
    builder.add(types.KeyboardButton(text='Покажи рецепты'))

    await message.answer(f'Как вам такие варианты: {recipe_translator.text}',
                        reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(RecipeState.waiting_for_recipe.state)

@router.message(RecipeState.waiting_for_recipe)
async def recipe_by_date(message: types.Message, state: FSMContext):
    translator = Translator()
    data_state = await state.get_data()
    id = data_state['id']
    recipe_Ingredient = []
    for id_t in id:
        async with aiohttp.ClientSession().get (url=f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={id_t}') as resp:
                   data = await resp.json()
                   recipe_name = [category['strMeal'] for category in data['meals']]
                   recipe_Instructions = [category['strInstructions'] for category in data['meals']]
                   for i in range(1, 21):
                       ingredients = [category[f'strIngredient{i}'] for category in data['meals']]
                       if any(ingredient and ingredient.strip() for ingredient in ingredients):
                           recipe_Ingredient.append(ingredients)

        recipe_name_j = ','.join(map(str, recipe_name))
        recipe_Instructions_j = ','.join(map(str, recipe_Instructions))
        recipe_Ingredient_j = ','.join([','.join(map(str, ingredients)) for ingredients in recipe_Ingredient])

        recipe_name_t= translator.translate(f'{recipe_name_j}', dest='ru')
        recipe_Instructions_t = translator.translate(f'{recipe_Instructions_j}', dest='ru')
        recipe_Ingredient_t = translator.translate(f'{recipe_Ingredient_j}', dest='ru')

        recipe_Ingredient = []

        await message.answer(
            f'''{recipe_name_t.text}
            \nРецепт:\n{recipe_Instructions_t.text}
            \nИнгридиенты:\n{recipe_Ingredient_t.text}
        '''
        )
