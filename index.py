from fastapi import FastAPI
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
                # c.Link(components=[c.Text(text='Назад')], on_click=BackEvent()),
                # c.Button(text="Получить данные", on_click=PageEvent(name="add-table")),
                c.Table(
                    data=users,
                    data_model=Model,
                    columns=[
                        DisplayLookup(field='ticker_m'),
                        DisplayLookup(field='shortname_m'),
                        DisplayLookup(field='lotsize_m'),
                        DisplayLookup(field='minstep_m'),
                        DisplayLookup(field='issuesize_m'),
                        DisplayLookup(field='isin_m'),
                        DisplayLookup(field='regnumber_m'),
                        DisplayLookup(field='listlevel_m'),
                        # DisplayLookup(field='close'),
                        # DisplayLookup(field='name', on_click=GoToEvent(url='/user/{id}/')),
                        # DisplayLookup(field='dob', mode=DisplayMode.date),
                    ],
                )

            ]
        )
    ]


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))


@app.get('/api/data/add', response_model=FastUI, response_model_exclude_none=True)
def add_data():
    return [
        c.Page(
            components=[
                # c.Link(components=[c.Text(text='Назад')], on_click=BackEvent()),
                # c.Heading(text='Данные с Московской биржи', level=2),
                # c.Table(
                #     data=all_stocks,
                #     # data_model=User,
                #     columns=[
                #         DisplayLookup(field='open'),
                #         DisplayLookup(field='close'),
                #         # DisplayLookup(field='name', on_click=GoToEvent(url='/user/{id}/')),
                #         # DisplayLookup(field='dob', mode=DisplayMode.date),
                #     ],
                # )
                c.Button(text="Обновить", on_click=GoToEvent(url="/data/add")),
            ]
        )
    ]
