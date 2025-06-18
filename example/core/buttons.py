from .functions import GenerateButton

Menu = GenerateButton(
    [
        {
            '📍 Pin Settings 📍': 'pinSettings'
        },
        {
            '➕ Add Admin': 'addAdmin',
            'Remove Admin ➖': 'removeAdmin'
        },
        {
            '⚙️ Control Pins ⚙️': 'controlPanel'
        }
    ]
)

PinSettings = GenerateButton(
    [
        {
            '➕ Add Pin': 'addPin',
            'Remove Pin ➖': 'removePin'
        },
        {
            '🔙': 'back'
        }
    ]
)

back = GenerateButton(
    [
        {
            '🔙': 'back'
        }
    ]
)