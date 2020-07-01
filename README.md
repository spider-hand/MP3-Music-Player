# MP3 Music Player
MP3 player inspired by iTunes.  

## Demo

<img src="../master/demo/demo.gif" height="450" />

## Set up
```
git clone https://github.com/spider-hand/MP3-Music-Player.git
pip install pyinstaller
pyinstaller main.py
```
You need to modify `main.spec` once after generating the application.

`main.spec`

```
added_files = [
    ('./app', 'app'),
    ('./images', 'images'),
]
    
a = Analysis(
    datas=added_files,
    ...
)
```

After modifying `main.spec` file, generate the application again.

```
pyinstaller --windowed --noconsole --clean --onefile main.spec
```

Now you can run `main.exe` file generated in `dist/main` folder.

Note: You can replace the artwork (`images/artwork/artwork.gif`) depening on the songs you want to play.
