from celery import shared_task
from time import sleep

import pandas as pd

from users.models import User
from admin_settings.models import Category, SubCategory
from products.models import Product

from django_base.settings import BASE_DIR

# function made to make a first test with celery
@shared_task
def sleep_message():
    sleep(5)
    return 'after sleeeeep'

@shared_task
def load_products(user_pk):
    user = User.objects.get(pk=user_pk)
    df = pd.read_csv('products.csv')
    products_names = Product.objects.values_list('name', flat=True)
    products_to_create = []
    
    for i, row in df.iterrows():
        if not all([
                not pd.isna(row['Product Name']),
                not pd.isna(row['Uniq Id']),
                not pd.isna(row['Selling Price']),
                not pd.isna(row['About Product']),
                not pd.isna(row['Category']),
            ]):
            continue # skip this row if any of the above field is empty

        if row['Product Name'] in products_names:
            print('product already exists ', row['Product Name'])
            continue
        try:
            price = float(row['Selling Price'].replace('$', '').split(' ')[0])
        except:
            continue

        category = Category.objects.get_or_create(name=row['Category'].replace(' | ', '|').split('|')[0])[0]
        subcategory = SubCategory.objects.get_or_create(name=row['Category'].replace(' | ', '|').split('|')[-1], category=category)[0]

        products_to_create.append(
            Product(
                name = row['Product Name'],
                owner = user,
                SKU = row['Uniq Id'],
                price = price,
                description = row['About Product'],
                category = category,
                subcategory = subcategory,
                )
        )

    Product.objects.bulk_create(products_to_create)

    return f'products created {len(products_to_create)}'