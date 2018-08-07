# DATA STATS
Explore quickly your data to get some statistical information about what you arte going to play with.

### Some commands to extract stats from a given corpus

To display total size per extension
```shell
find . -type f |  egrep -o "\.[a-zA-Z0-9]+$" | sort -u | xargs -I '%' find . -type f -name "*%" -exec du -ch {} + -exec echo % \; | egrep "^\.[a-zA-Z0-9]+$|total$" | uniq | paste - -
```

To get detailed meta data
```shell
find . -type f -print0 | xargs -0 file  | cut  -d':' -f2- | sed -e "s/^ \{1,\}//" 
```

To get MIME type and charset info
```shell
find . -type f -print0 | xargs -0 file -i
```
To get count of MIME types
```shell
find . -type f -print0 | xargs -0 file -bi | cut -f1 -d';' | sort | uniq -c
```
To get file size and modification date
```shell
find . -type f -print0 | xargs -0 stat --format="%n|%s|%y" 
```

To find duplicates:
 * filename
```shell
find . -type f -printf "%f\n" | grep -o ".*\." | sort | uniq -c | awk '$1>1 {print;}'
```
* filename with extension
```shell
find . -type f -printf "%f\n" | sort | uniq -c | awk '$1>1 {for (f=2; f<=NF; ++f) {printf("%s ",$f);}; printf("|%s\n",$1)}'
```

* filename with extension and size in bytes
```shell
find . -type f -print0 | xargs -0 stat --format="%n|%s" | awk -F "/" '{print $NF}' | sort | uniq -c |awk '$1>1 {for (f=2; f<=NF; ++f) {printf("%s ",$f);}; printf("|%s\n",$1)}'
```

To count number of times a word occurs as is:
```shell
find . -type f -print0 | xargs -0 grep -wc keyword | cut -f2 -d':' | awk '{s+=$1} END {print s}'
```
