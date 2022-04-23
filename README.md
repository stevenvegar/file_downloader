# file_downloader
Python script for download files from internet

Very useful when connection or server aren't stable.

The script request the file size in bytes to the server,
then checks if the file exist in the local storage, if so,
read its size and compare if it is completely downloaded, if not,
starts to download from the remaining bytes.
At the end, shows the MD5 and SHA256 sums.Cancel changes

When the connection is timed out (30s) due to a network issue,
it retries the download process, until the file is complete.

### Usage:
 python3 downloader.py URL_of_file_to_download
 
![screenshot](https://myoctocat.com/assets/images/base-octocat.svg)



### TODO:
- Add support to multiple URLs in text file.
- Add checking with a supplied hash sum.
- Parallel downloadings.
