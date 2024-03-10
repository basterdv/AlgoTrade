from fastapi import FastAPI, HTTPException
from fastui import FastUI, components as c, AnyComponent, prebuilt_html
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent, PageEvent
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


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def index() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Heading(text='Алго данные с Московской биржи', level=2),
                c.Table(
                    data=users,
                    data_model=Model,
                    columns=[
                        DisplayLookup(field='ticker_m', on_click=GoToEvent(url='/ticker/{ticker_m}')),
                        DisplayLookup(field='shortname_m'),
                        DisplayLookup(field='lotsize_m'),
                        DisplayLookup(field='minstep_m'),
                        DisplayLookup(field='issuesize_m'),
                        DisplayLookup(field='isin_m'),
                        DisplayLookup(field='regnumber_m'),
                        DisplayLookup(field='listlevel_m', table_width_percent=5),

                    ],
                )

            ]
        )
    ]


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
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))
