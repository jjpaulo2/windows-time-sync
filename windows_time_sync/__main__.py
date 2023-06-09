from asyncio import new_event_loop
from windows_time_sync.main import main


if __name__ == '__main__':
    loop = new_event_loop()
    loop.run_until_complete(main())
    