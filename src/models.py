from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    link = Column(String, nullable=False)

    currency_id = Column(Integer, ForeignKey("currency.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("product_type.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("product_source.id"), nullable=False)

    calories = Column(Integer)
    total_fat = Column(Integer)
    total_carb = Column(Integer)
    total_protein = Column(Integer)
    vitamin_d = Column(Integer)
    calcium = Column(Integer)
    iron = Column(Integer)
    potassium = Column(Integer)
    available = Column(Boolean, default=True)

    currency = relationship("Currency", back_populates="products")
    type_ = relationship("ProductType", back_populates="products")
    source = relationship("ProductSource", back_populates="products")

    eat_list_products = relationship("EatListProduct", back_populates="product")


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, index=True)
    quote = Column(String, nullable=False)

    products = relationship("Product", back_populates="currency")


class ProductType(Base):
    __tablename__ = "product_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    products = relationship("Product", back_populates="type_")


class ProductSource(Base):
    __tablename__ = "product_source"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)

    products = relationship("Product", back_populates="source")


class UserProduct(Base):
    __tablename__ = "user_product"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    special_name = Column(String)
    like = Column(Boolean)
    recommend = Column(Boolean)
    reason = Column(String)


class EatList(Base):
    __tablename__ = "eat_list"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)


class EatListProduct(Base):
    __tablename__ = "eat_list_product"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False, default=1)
    eat_list_id = Column(Integer, ForeignKey("eat_list.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)

    product = relationship("Product", back_populates="eat_list_products")


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id"), unique=True, nullable=False
    )
    weight = Column(Float)
    age = Column(Integer)
    activity = Column(Float)
