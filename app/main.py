from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select
from pathlib import Path
from app.book_scraper import NaverBookScraper
from app.models import mysql_db, Base
from app.models.book import BookModel
import asyncio

BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)

app = FastAPI(title='Book Collector', version='0.0.1')
templates = Jinja2Templates(directory=BASE_DIR / 'templates')

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    '''
    Render the main page
    '''
    context = {'request': request, 'title': 'Book Collector'}
    return templates.TemplateResponse('index.html', context=context)
    
    
@app.get('/search', response_class=HTMLResponse)
async def search_result(request: Request):
    keyword = request.query_params.get('q')
    if not keyword:
        context = {'request': request}
        return templates.TemplateResponse('index.html', context=context)
    
    async with mysql_db.session_local() as session:  
        naver_book_scraper = NaverBookScraper()
        scraped_books = await naver_book_scraper.search(keyword, 10)
        
        book_models = []
        for book in scraped_books:
            book_model = BookModel(
                keyword=keyword,
                publisher=book['publisher'],
                price = int(book['discount']),
                image=book.get('image', ''),  # Safely handle missing image
            )
            book_models.append(book_model)
            session.add(book_model)  
        await session.commit()  
        
        context = {"request": request, "keyword": keyword, "books": scraped_books}
        return templates.TemplateResponse("index.html", context=context)

@app.on_event('startup')
async def on_app_start():
    '''
    Triggered before the app starts
    '''
    mysql_db.connect()
    # Create database tables
    async with mysql_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event('shutdown')
async def on_app_shutdown():
    '''
    Triggered after the app shuts down.
    Close the MySQL connection.
    '''
    await mysql_db.close()
