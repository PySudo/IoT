from .core import (
    DB,
    isValid,
    app,
    Body
)

@app.get('/AddPin')
async def AddPin(key: str, GPIO: int, name: str):
    if not isValid(key):
        return {'ok': False, 'error': 1}
    result = await DB.addPin(GPIO, name)
    return {'ok': result}

@app.get('/DelPin')
async def AddPin(key: str, GPIO: int):
    if not isValid(key):
        return {'ok': False, 'error': 1}
    result = await DB.delPin(GPIO)
    return {'ok': result}

@app.get('/ChangeValue')
async def ChangeValue(key: str, GPIO: int, value: int = None):
    if not isValid(key):
        return {'ok': False, 'error': 1}

    if not value in (0,1) and value is not None:
        return {'ok': False, 'error': 3} 

    result = await DB.ChangeValue(GPIO, value)
    if result is False:
        return {'ok': False, 'error': 2}
    return {'ok': result}

@app.get('/GetPins')
async def GetPins(key: str):
    if not isValid(key):
        return {'ok': False, 'error': 1}

    return {'ok': True, 'result': (await DB.GetAllPins())}