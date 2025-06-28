from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///example.db', echo=False)

Base = declarative_base()

# to talk to database
Session = sessionmaker(bind=engine)
session = Session()


class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)

    # back reference
    products = relationship('Product', back_populates='category')


class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'))

    # so each Product knows its Category
    category = relationship('Category', back_populates='products')

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
#  Category instances
c1 = Category(category_name='Electronics')
c2 = Category(category_name='Books')

#  Product instances
p1 = Product(product_name='Wireless Mouse', price=19.99, category=c1)
p2 = Product(product_name='Mechanical Keyboard', price=49.99, category=c1)
p3 = Product(product_name='Science Fiction Novel', price=12.50, category=c2)
p4 = Product(product_name='Data Science Handbook', price=25.00, category=c2)


session.add_all([c1, c2, p1, p2, p3, p4])
session.commit()

products = session.query(Product).all()

for prod in products:
    print(f"Product: {prod.product_name} | Price: ₹{prod.price:.2f} | Category: {prod.category.category_name}")
