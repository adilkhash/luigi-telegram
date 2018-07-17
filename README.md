# luigi-telegram
Luigi Tasks status notifications to Telegram

## Usage
```python
if __name__ == '__main__':
    with LuigiTelegramNotification('my_bot_token', 1234567):
        luigi.run()
```
