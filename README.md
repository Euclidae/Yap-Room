# Chat Room

A simple Python chat room with a GUI client and server. Nothing fancy, just works.
![image](https://github.com/user-attachments/assets/e70d2e02-7101-4fe6-a5ad-9b5afadae9cb)


## What it is

- `server.py` - Basic chat server that handles multiple clients
- `client.py` - GUI chat client using customtkinter
- Dark theme because light themes hurt my eyes
- Tested on Arch Linux btw

## Requirements

```bash
pip install customtkinter
```

That's it. Everything else is standard Python stuff.

## How to use

1. Start the server first:
```bash
python server.py
```

2. Run the client(s):
```bash
python client.py
```

3. Enter your username when prompted
4. Chat away
5. Type `#quit` to leave

## Known Issues

- Messages sometimes appear twice when you send them (see screenshot). Still figuring out why this happens but it's just a display thing - the actual message only gets sent once to other clients.
  ![image](https://github.com/user-attachments/assets/08d9903d-d6bf-4ae7-b71e-7303af1189d9)

## Features

- Multiple clients can connect
- Real-time messaging
- Timestamps on messages
- Handles client disconnections gracefully
- Resizable window
- Dark theme (obviously)

## Connection Info

- Default host: localhost
- Default port: 8080
- You can change these in the code if needed

## License
MIT Licese
Do whatever you want with it. Use it, modify it, break it, fix it - I don't care. No warranty or anything like that.

## Author

Made by Euclidae

---

*If you find bugs or want to improve something, go ahead. The code isn't perfect but it works.*
