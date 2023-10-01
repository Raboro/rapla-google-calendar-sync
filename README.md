# Rapla-Google-Calendar-Sync

Automatically fetch [Rapla](https://rapla.org/) calendar events and save them into [Google Calendar](https://calendar.google.com/).  

## Install dependencies
```bash
$ pip install -r requirements.txt
```

or 
```bash
$ make install
```


## Run Code
```bash
$ python src/main.py
```

or 
```bash
$ make run
```

## Config
You need to set the url to fetch the rapla calendar. You need to also provide you google calendar name and your time zone. This all is set in the ``.env`` file. Example of this is ``example.env``.
You also need ti gave your credentials you set in the ``credentials.json`` (Example is called ``credentials.example.json``). See more [here](https://www.youtube.com/watch?v=B2E82UPUnOY&) to learn more about the credentials and how to get them. 