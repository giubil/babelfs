# Babelfs

This is a filesystem based on the Library Of Babel website, where your files are stocked in the library, and the filesystem does not contain any data, only metadata.

## Installing 

```
virtualenv -p $(which python2) venv/
source venv/bin/activate.sh
pip install -r requirements.txt
```

Note that you must have fuse installed for it to work.

## Usage

```
python babelfs.py metadataStorageFolder/ mountPoint/ 
```

## Notes

This is a very inefficient FileSytem. But it does not stock any data, only metadata (tho the metadata takes about twice the space as the actual data).

It is painfully slow (about 4ko/s read speed and 3ko/s write speed), and actually uploads all of your data to [the library of babel](https://libraryofbabel.info/). Because their algorithm is not open source, I have to do it that way. So please do not store any confidential documents on this fs, because they will be sent to this website.

Please do not store ANY important files that you do not have backups of on this filesystem. Writing at a random offset is not yet supported (dd uses writes offest, cp does not) so some programs may not work. A lot of error handling is not implemented yet, so there is a real chance that you may loose your files.

This is just for fun, and is not intended to be a viable fs, so please do not use it that way.