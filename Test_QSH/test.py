import requests
from bs4 import BeautifulSoup as BS



app = FastAPI()

r = requests.get("http://erinrv.qscalp.ru/")
html = BS(r.content, 'html.parser')

r2 = str(r)

if r2 == '<Response [200]>':
    print('connect OK')

listDir = []
listSec = []

allDir = html.findAll('a')  # soup.findAll('a', class_='lenta')

for data in allDir:
    listDir.append(data.text)

dir = listDir[len(listDir) - 1]

r_dir = requests.get(f'http://erinrv.qscalp.ru/{dir}/')
html = BS(r_dir.content, 'html.parser')
allSec = html.findAll('a')

for data in allSec:
    listSec.append(data.text)

for link in html.find_all('a'):
    if link.get('href') != '/':
        print(link.get('href'))

# Скачиваем файл
file1 = requests.get('http://erinrv.qscalp.ru/2024-04-03/VTBR.2024-04-03.Deals.qsh')

with open('Test_QSH/VTBR.2024-04-03.Deals.qsh', 'wb') as file:
    file.write(file1.content)

users = []


class Model(BaseModel):
    id: int = Field(title='№')
    ticker_m: str = Field(title='Тикер')


class FilterForm(BaseModel):
    ticker_id: int = Field()


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def test2(page: int = 1, ticker_id: str | None = None) -> list[AnyComponent]:
    page_size = 20
    filter_form_initial = {'ticker_id': 3, 'dfdffd': 6}

    return [
        c.Page(
            components=[
                c.Heading(text='Алго данные с Московской биржи', level=2),
                c.ModelForm(
                    model=FilterForm,
                    submit_url='.',
                    initial=filter_form_initial,
                    method='GOTO',
                    submit_on_change=True,
                    # display_mode='inline',
                ),
                c.Table(
                    data=users[(page - 1) * page_size:page * page_size],
                    data_model=Model,

                ),
                c.Pagination(page=page, page_size=page_size, total=len(users)),
            ]
        )
    ]


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='Получение исторических данных'))

# print(html.prettify())
# print(html.a)