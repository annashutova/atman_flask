from app.extensions import db
from app.models import Category


def add_mock_categories():
    main_categories = [
        ('Бумага', 'paper.jpg'),
        ('Картриджи и тонеры', 'printers_cartridges.jpg'),
        ('Офисные принадлежности', 'stationary.jpg'),
        ('Товары для уборки офиса и сангигиены', 'cleaning_supplies.jpg')
    ]

    paper_categories = [
        ('Белая бумага', 'white_paper.jpg'),
        ('Цветная бумага ', 'color_paper.jpg'),
        ('Чековая лента', 'receipt_tape.jpg'),
        ('Наклейки', 'stickers.jpg'),
        ('Разная', 'other_paper.jpg'),
        ('Рулонная бумага', 'coiled_paper.jpg'),
        ('Фотобумага', 'photo_paper.jpg'),
        ('Этикет-лента, термоэтикетки, ценники', 'price_tags_paper.jpg'),
    ]

    for title, image in main_categories:
        category = Category(title=title, image=image, master_category=None)
        db.session.add(category)

    paper = Category.query.filter_by(title = 'Бумага').first()
    for title, image in paper_categories:
        category = Category(title=title, image=image, master_category=paper.id)
        db.session.add(category)

    try:
        db.session.commit()
    except Exception as error:
            print(error)
