from flask import Blueprint, render_template, request, redirect, url_for
from ...models.product import Product, ProductModel, ProductSize
from ...controllers.products_controller import getProducts, getProductById, insertProduct, updateProduct, deleteProduct
from ...models.db import db
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from ...controllers.products_controller import convertImageToBase64
import base64
import logging

products = Blueprint('products', __name__, url_prefix='/admin/products')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

@products.route('/products-index')
@login_required
@roles_required('admin')
def index():
    # products = getProducts(1)
    products = ProductModel.query.filter_by(status=1)
    logger.info('Se muestran los productos activos: %s', current_user.name)
    return render_template('/admin/products/index_product.html', products=products)


@products.route('/products-insert', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def insert():
    if (request.method == 'POST'):
        name = request.form.get('txtName')
        description = request.form.get('txtDescription')
        price = request.form.get('txtPrice')
        size = request.form.get('cmbSize')
        min_value = request.form.get('txtMinValue')
        max_value = request.form.get('txtMaxValue')
        # quantity = request.form.get('txtQuantity')
        filename = request.files['photo']

        # product = Product(0, '', name, description, price,
        #                 size, min_value, max_value, quantity, filename.filename)
        # insertProduct(product)
        # print('inserting product')
        product = ProductModel(
            sku=name,
            name=name,
            description=description,
            price=price,
            size='',
            min_value=min_value,
            max_value=max_value,
            photo=convertImageToBase64(),
            status=1
        )

        db.session.add(product)
        logger.info('Se agrega correctamente un producto: %s', current_user.name)
        db.session.commit()

        return redirect(url_for('products.index'))

    return render_template('/admin/products/insert_product.html')


@products.route('/products-update/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def update(id):
    if (request.method == 'GET'):
        # response = getProductById(id)
        product = ProductModel.query.get(id)
        return render_template('/admin/products/update_product.html', product=product)

    if (request.method == 'POST'):
        id = request.form.get('txtId')
        sku = request.form.get('txtSku')
        name = request.form.get('txtName')
        description = request.form.get('txtDescription')
        price = request.form.get('txtPrice')
        size = request.form.get('cmbSize')
        min_value = request.form.get('txtMinValue')
        max_value = request.form.get('txtMaxValue')
        quantity = request.form.get('txtQuantity')
        filename = request.files['photo']
        product = Product(id, sku, name, description, price,
                          size, min_value, max_value, quantity, filename)
        updateProduct(product)
        logger.info('Se modifica correctamente un producto: %s', current_user.name)
        return redirect(url_for('products.index'))


@products.get('/products-delete/<int:product_id>')
@login_required
@roles_required('admin')
def delete(product_id):
    deleteProduct(product_id)
    logger.info('Se elimina correctamente un producto: %s', current_user.name)
    return redirect(url_for('products.index'))
