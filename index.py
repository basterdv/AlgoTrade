from collections import defaultdict

import pydantic
from fastapi import FastAPI, HTTPException, Request
from fastui import FastUI, components as c, AnyComponent, prebuilt_html
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent, PageEvent
from fastui.forms import SelectSearchResponse
from httpx import AsyncClient
from pydantic import BaseModel, ConfigDict, ValidationError, Field
from starlette.responses import HTMLResponse
from main import All_stocks

app = FastAPI()

st = All_stocks()
table = st.get_table()

ticker = table['ticker']
shortname = table['shortname']
lotsize = table['lotsize']
minstep = table['minstep']
issuesize = table['issuesize']
isin = table['isin']
regnumber = table['regnumber']
listlevel = table['listlevel']


class Model(BaseModel):
    id: int = Field(title='№')
    ticker_m: str = Field(title='Тикер')
    shortname_m: str = Field(title='Короткое наименование')
    lotsize_m: int = Field(title='Размер лота')
    minstep_m: float = Field(title='Минимальный шаг')
    issuesize_m: int = Field(title='Размер выпуска')
    isin_m: str = Field(title='Код ценной бумаги')
    regnumber_m: str = Field(title='Рег номер')
    listlevel_m: int = Field(title='Уровень листинга')


users = []

# Формируе картэж тикеров
for i in ticker:
    users.append(
        Model(
            id=i + 1,
            ticker_m=ticker[i],
            shortname_m=shortname[i],
            lotsize_m=lotsize[i],
            minstep_m=minstep[i],
            issuesize_m=issuesize[i],
            isin_m=isin[i],
            regnumber_m=regnumber[i],
            listlevel_m=listlevel[i],
        ),
    )


class FilterForm(BaseModel):
    # ticker_id: int = Field()

    ticker_id: int = Field()

    # ticker_id: str = Field(json_schema_extra={'search_url': '/api/search', 'placeholder': 'Фильтр по уровню '
    #                                                                                       'листинга...'})


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def index(page: int = 1, ticker_id: str | None = None) -> list[AnyComponent]:
    page_size = 20
    filter_form_initial = {'ticker_id': 3, 'dfdffd': 6}

    # if ticker_id:
    #     tickers = [y for y in users if y.ticker_m == ticker_id]
    #     print(tickers)
    #     ticker_name = users[0].ticker_m if tickers else ticker_id
    #     filter_form_initial = {'value': 'ticker_id', 'label': 'ticker_name'}

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
                    columns=[
                        DisplayLookup(field='id'),
                        DisplayLookup(field='ticker_m', on_click=GoToEvent(url='/ticker/{ticker_m}')),
                        DisplayLookup(field='shortname_m'),
                        DisplayLookup(field='lotsize_m'),
                        DisplayLookup(field='minstep_m'),
                        DisplayLookup(field='issuesize_m'),
                        DisplayLookup(field='isin_m'),
                        DisplayLookup(field='regnumber_m'),
                        DisplayLookup(field='listlevel_m', table_width_percent=5),
                    ],
                ),
                c.Pagination(page=page, page_size=page_size, total=len(users)),
            ]
        )
    ]


@app.get('api/search', response_model=SelectSearchResponse)
async def search_view(request: Request, q: str) -> SelectSearchResponse:
    options = [{'label': 'k', 'options': 'v'}]
    path_ends = f'name/{q}' if q else 'all'

    return SelectSearchResponse(options=options)


# async def search_view(request: Request, q: str) -> SelectSearchResponse:
#     path_ends = f'name/{q}' if q else 'all'
#     client: AsyncClient = request.app.state.httpx_client
#     r = await client.get(f'https://restcountries.com/v3.1/{path_ends}')
#     if r.status_code == 404:
#         options = []
#     else:
#         r.raise_for_status()
#         data = r.json()
#         if path_ends == 'all':
#             # if we got all, filter to the 20 most populous countries
#             data.sort(key=lambda x: x['population'], reverse=True)
#             data = data[0:20]
#             data.sort(key=lambda x: x['name']['common'])
#
#         regions = defaultdict(list)
#         for co in data:
#             regions[co['region']].append({'value': co['cca3'], 'label': co['name']['common']})
#         options = [{'label': k, 'options': v} for k, v in regions.items()]
#     return SelectSearchResponse(options=options)


@app.get('/api/ticker/{ticker_m}', response_model=FastUI, response_model_exclude_none=True)
def profile_ticker(ticker_m: str) -> list[AnyComponent]:
    try:
        ticker_id = next(u for u in users if u.ticker_m == ticker_m)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Ticker not found")
    return [
        c.Page(
            components=[
                c.Heading(text=f'({ticker_id.ticker_m}) {ticker_id.shortname_m}', level=2),
                c.Details(data=ticker_id),
                c.Link(components=[c.Text(text='Назад')], on_click=BackEvent()),
            ]
        ),
    ]


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='ALGO MOEX'))
