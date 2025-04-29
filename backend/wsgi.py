from app import create_app
from app.config import DevelopmentConfig, TestingConfig, ProductionConfig

app = create_app(ProductionConfig)